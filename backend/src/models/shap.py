import shap

import numpy as np

from abc import ABC
from enum import Enum, auto
from xgboost import DMatrix

class Model(ABC):
    def predict(X, *args):
        pass

class ModelKind(Enum):
    SklearnLinear = auto()
    SklearnTree = auto()
    XGBoostTree = auto()
    Custom = auto()
    
class ShapelyExplainer:
    def __init__(self, trained_model: Model, model_kind: ModelKind, background_data=None):
        """
        Initialize Explainer Instance
        :param trained_model: A fitted model (must implement .predict)
        :param model_kind: The kind of model being explained
        :param background_data: Optional representative background dataset (e.g., X_train)
        """
        self.model = trained_model
        self.model_kind = model_kind
        self.background_data = background_data
        self._explainer = None
        self._init_explainer()

    # ---------------------------------------------------------------
    # Core initialization logic
    # ---------------------------------------------------------------
    def _init_explainer(self):
        match self.model_kind:
            # -----------------------------
            # LINEAR MODELS (e.g. LogisticRegression)
            # -----------------------------
            case ModelKind.SklearnLinear:
                if self.background_data is None:
                    raise ValueError("For LinearExplainer, provide background data (i.e a small subset of the training dataset)")
                masker = shap.maskers.Independent(self.background_data)
                self._explainer = shap.LinearExplainer(self.model, masker=masker)
                self.explain_prediction = self._explain_linear

            # -----------------------------
            # TREE MODELS (e.g. RandomForest, GradientBoosting)
            # -----------------------------
            case ModelKind.SklearnTree:
                self._explainer = shap.TreeExplainer(self.model)
                self.explain_prediction = self._explain_tree

            # -----------------------------
            # XGBOOST MODELS
            # -----------------------------
            case ModelKind.XGBoostTree:
                self.booster = self.model.get_booster()
                self.explain_prediction = self._explain_xgboost

            # -----------------------------
            # CUSTOM MODELS (black-box)
            # -----------------------------
            case ModelKind.Custom:
                if self.background_data is None:
                    raise ValueError("background_data must be provided for KernelExplainer.")
                masker = shap.maskers.Independent(self.background_data)
                self._explainer = shap.KernelExplainer(self.model.predict, masker)
                self.explain_prediction = self._explain_custom

            case _:
                raise ValueError(f"Unsupported model kind: {self.model_kind}")
    
    # ---------------------------------------------------------------
    # Explainer methods for each model type
    # ---------------------------------------------------------------
    def _explain_linear(self, X):
        """SHAP values for linear models"""
        shap_values = self._explainer(X)
        return shap_values.values  # shape (nsamp, nfeats)

    def _explain_tree(self, X):
        """SHAP values for tree-based sklearn models"""
        shap_values = self._explainer.shap_values(X)
        return self._process_output(shap_values)

    def _explain_xgboost(self, X):
        """SHAP values for XGBoost models"""
        shap_values = self.booster.predict(DMatrix(X), pred_contribs=True)

        if shap_values.ndim == 3:
            # shape: (nsamp, nclass, nfeats + 1)
            shap_values = shap_values[:, :, :-1]  # remove bias
            shap_values = shap_values.transpose((0, 2, 1))  # (nsamp, nfeats, nclass)
        else:
            shap_values = shap_values[:, :-1]  # (nsamp, nfeats)
        return shap_values

    def _explain_custom(self, X):
        """SHAP values for black-box models (approximate, slow)"""
        shap_values = self._explainer.shap_values(X)
        return self._process_output(shap_values)

    # ---------------------------------------------------------------
    # Utility for unifying SHAP output shapes
    # ---------------------------------------------------------------
    def _process_output(self, shap_values):
        """Ensure consistent (nsamp, nfeats) shape for binary classifiers."""
        if isinstance(shap_values, list):
            # If it's a list of arrays (e.g., [class0, class1])
            if len(shap_values) == 2:
                return shap_values[1]  # Positive class
            else:
                # Multi-class (n_classes > 2)
                shap_values = np.stack(shap_values, axis=-1)  # (nsamp, nfeats, nclass)
        return shap_values