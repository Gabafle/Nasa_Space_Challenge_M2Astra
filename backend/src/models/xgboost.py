import pandas as pd
import numpy as np
# Assurez-vous d'avoir les imports des classes ShapelyExplainer et ModelKind disponibles
# from .ShapelyExplainer import ShapelyExplainer, ModelKind # Si c'était un module
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from typing import Union
from backend.src.models.shap import  ModelKind, ShapelyExplainer
# Note: La classe ModelKind et ShapelyExplainer doivent être définies 
# avant d'utiliser la classe XGBoostModel.

class XGBoostModel:
    """
    Une interface pour le modèle de Classification XGBoost qui gère la standardisation
    et intègre l'explication SHAP après l'entraînement.
    """
    
    def __init__(self, n_estimators=100, max_depth=6, learning_rate=0.1, 
                 random_state=None, n_jobs=-1, **kwargs):
        """
        Initialise le modèle XGBClassifier.
        """
        self.model = XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            n_jobs=n_jobs,
            use_label_encoder=False, 
            eval_metric='mlogloss',
            **kwargs
        )
        
        self.scaler = StandardScaler()
        self.explainer = None  # Contiendra l'instance ShapelyExplainer
        self.shap_values = None  # Contient les valeurs SHAP globales (ex: pour le X_train)

    def train(self, X_train: Union[np.ndarray, pd.DataFrame], y_train: Union[np.ndarray, pd.Series]):
        """
        Standardise, entraîne le modèle, et initialise l'explainer SHAP.
        """
        if isinstance(X_train, pd.DataFrame):
            # Le scaler de Sklearn préfère les tableaux numpy
            X_train_np = X_train.values 
        else:
            X_train_np = X_train
            
        # 1. Standardisation
        X_train_scaled = self.scaler.fit_transform(X_train_np)
        
        # 2. Entraînement du modèle XGBoost
        self.model.fit(X_train_scaled, y_train)
        
        # 3. Initialisation de l'explainer SHAP (XGBoostTree)
        # Note: Nous passons le modèle entraîné à l'explainer
        # Nous utilisons X_train_scaled comme background_data car c'est la forme vue par le modèle
        
        # Le background_data doit être un numpy array pour l'explainer
        self.explainer = ShapelyExplainer(
            trained_model=self.model, 
            model_kind=ModelKind.XGBoostTree,
            # Le modèle a été entraîné sur des données standardisées, 
            # donc nous passons les données standardisées.
            background_data=X_train_scaled 
        )
        
        # 4. Calcul des valeurs SHAP globales sur le jeu d'entraînement (Optionnel)
        # Ces valeurs sont utiles pour les graphiques de résumé globaux.
        self.shap_values = self.explainer.explain_prediction(X_train_scaled)


    def predict(self, X_test: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Standardise les nouvelles données et prédit leurs classes.
        """
        if isinstance(X_test, pd.DataFrame):
            X_test_np = X_test.values
        else:
            X_test_np = X_test
            
        # Standardise les données de test (transform)
        X_test_scaled = self.scaler.transform(X_test_np)
        
        # Fait la prédiction
        return self.model.predict(X_test_scaled)

    # ... (predict_proba, get_params, set_params restent inchangées)
    
    def get_feature_contributions(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Calcule et retourne les valeurs SHAP pour un ensemble de données X donné.
        """
        if self.explainer is None:
            raise AttributeError("Le modèle doit être entraîné avant de calculer les contributions SHAP.")
            
        if isinstance(X, pd.DataFrame):
            X_np = X.values
        else:
            X_np = X

        # Standardise les données avec le scaler appris lors de l'entraînement
        X_scaled = self.scaler.transform(X_np)
        
        # Retourne les valeurs SHAP en utilisant l'explainer interne
        return self.explainer.explain_prediction(X_scaled)


    def predict_proba(self, X_test: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Standardise les nouvelles données et prédit leurs probabilités de classe.
        """
        if isinstance(X_test, pd.DataFrame):
            X_test_np = X_test.values
        else:
            X_test_np = X_test
            
        X_test_scaled = self.scaler.transform(X_test_np)
        return self.model.predict_proba(X_test_scaled)

    def get_params(self, deep=True):
        """Retourne les paramètres du modèle Scikit-learn, nécessaire pour GridSearchCV."""
        return self.model.get_params(deep=deep)

    def set_params(self, **params):
        """Définit les paramètres du modèle Scikit-learn, nécessaire pour GridSearchCV."""
        return self.model.set_params(**params)