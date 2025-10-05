import pandas as pd
import numpy as np
# Assurez-vous d'avoir les imports des classes ShapelyExplainer et ModelKind disponibles
# from .ShapelyExplainer import ShapelyExplainer, ModelKind # Si c'était un module
from xgboost import XGBClassifier, Booster
from sklearn.preprocessing import StandardScaler
from typing import Union
from backend.src.models.shap import  ModelKind, ShapelyExplainer
# Note: La classe ModelKind et ShapelyExplainer doivent être définies 
# avant d'utiliser la classe XGBoostModel.

from scipy.special import softmax  # To apply softmax function

from backend.src.models.base_model import BaseModel



class XGBoostModel(BaseModel):
    """
    Une interface pour le modèle de Classification XGBoost qui gère la standardisation
    et intègre l'explication SHAP après l'entraînement.
    """
    
    def __init__(self):
        """
        Initialise le modèle XGBClassifier.
        """
        super().__init__()
        self.model = None
        
        self.scaler = StandardScaler()
        self.explainer = None  # Contiendra l'instance ShapelyExplainer

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


    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Standardise les nouvelles données, prédit les classes, et retourne un DataFrame
        contenant la classe prédite et les valeurs SHAP pour la Classe 2.
        """

        feature_names = [
            "pl_orbper",
            "pl_rade",
            "pl_tranmid",
            "pl_trandep",
            "st_teff",
            "st_rad",
            "st_logg",
            "ra",
            "dec",
        ]

        X_test = X[feature_names]
        
        X_test_np = X_test.values
        index_to_use = X_test.index
            
        # Standardise les données de test (transform)
        X_test_scaled = self.scaler.transform(X_test_np)
        
        # 1. Faire la prédiction de classe
        predictions = self.model.predict(X_test_scaled)
        
        # 2. Calculer les contributions SHAP (forme attendue : (N_samples, N_features, N_classes))
        # Nous appelons get_feature_contributions qui utilise l'explainer
        shap_values_all_classes = self.get_feature_contributions(X_test) 
        
        # --- Extraction des valeurs SHAP pour la Classe 2 (Index 2) ---
        # Si la forme est (N, F, C), on prend l'index 2.
        # Attention : C'est l'index 2 (la troisième classe) qui est demandée.
        try:
            shap_values_class_2 = shap_values_all_classes[:, :, 2] 
        except IndexError:
             # Gérer les cas où le modèle est binaire (N, F) ou n'a pas 3 classes
             # Nous gérons ici l'erreur pour garantir que la méthode ne plante pas.
             raise ValueError("Erreur SHAP : La 'Classe 2' (index 2) n'existe pas. Veuillez vérifier le nombre de classes de votre modèle.")

        # 3. Créer le DataFrame SHAP
        shap_df = pd.DataFrame(
            shap_values_class_2, 
            index=index_to_use, 
            columns=feature_names
        )
        
        # 4. Renommer les colonnes SHAP
        shap_df.columns = [f'{col}_SHAP' for col in shap_df.columns]
        
        proba = self.model.predict_proba(X_test)
        proba = pd.DataFrame(softmax(proba, axis=1), columns=[f'softmax_class_{i+1}' for i in range(proba.shape[1])], index=index_to_use)

        predictions = pd.Series(predictions, index=index_to_use, name='predicted_target')

        # 6. Combiner le tout (la prédiction et les valeurs SHAP)
        result_df = pd.concat([X, proba, shap_df, predictions], axis=1)
        
        return result_df

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

    def set_params(self, n_estimators=55, max_depth=9, learning_rate=0.1, random_state=None, n_jobs=-1, **kwargs):
        """Définit les paramètres du modèle Scikit-learn, nécessaire pour GridSearchCV."""
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
    
    def save_model(self, filepath: str):
        #self.model.get_booster().save_model(filepath)
        self.model.save_model(filepath)
        
    def load_model(self, file_paths) -> None:
        """
        Load_model
        """
        self.set_params()
        #booster = Booster()
        #booster.load_model(file_paths)
        self.model.load_model(file_paths)
        #self.model._Booster = booster