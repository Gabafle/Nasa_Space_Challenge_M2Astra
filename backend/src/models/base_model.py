from abc import ABC, abstractmethod
from typing import Union, Any
import pandas as pd
import numpy as np
import xgboost as xgb



class BaseModel(ABC):
    """
    Classe abstraite pour définir le contrat commun de tout modèle de Machine Learning.
    Elle gère les signatures des méthodes essentielles : entraînement, prédiction,
    et explication des prédictions via SHAP (ou tout autre mécanisme).
    """

    def __init__(self):
        """
        Initialise les composants de base communs à tous les modèles.
        """
        self.model: Any = None
        self.scaler: Any = None
        self.explainer: Any = None
        self.shap_values: Union[np.ndarray, None] = None

    # =======================================================================
    # 🔧 Méthodes abstraites (doivent être implémentées par les sous-classes)
    # =======================================================================

    @abstractmethod
    def train(self, X_train: Union[np.ndarray, pd.DataFrame],
              y_train: Union[np.ndarray, pd.Series]) -> None:
        """
        Entraîne le modèle sur les données fournies et initialise l'explainer SHAP.
        """
        pass

    @abstractmethod
    def predict(self, X_test: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Fait des prédictions sur un ensemble de données de test.
        """
        pass

    @abstractmethod
    def predict_proba(self, X_test: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Retourne les probabilités de chaque classe pour un ensemble de données donné.
        """
        pass

    @abstractmethod
    def get_feature_contributions(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Calcule les valeurs SHAP (ou équivalent) pour les données d'entrée X.
        """
        pass

    @abstractmethod
    def get_params(self, deep: bool = True):
        """
        Retourne les hyperparamètres du modèle (compatible Scikit-learn).
        """
        pass

    
    def load_model(self, file_paths) -> None:
        """
        Load_model
        """
        self.model = xgb.XGBClassifier()
        self.model.load_model(file_paths)
    
    
    def _check_trained(self):
        """
        Vérifie que le modèle a bien été entraîné avant utilisation.
        """
        if self.model is None:
            raise AttributeError("Le modèle doit être entraîné avant d’être utilisé.")

    def _to_numpy(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Convertit une DataFrame en numpy array pour compatibilité avec Sklearn/XGBoost.
        """
        if isinstance(X, pd.DataFrame):
            return X.values
        return X
