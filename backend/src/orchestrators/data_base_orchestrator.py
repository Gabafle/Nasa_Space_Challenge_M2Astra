from pydantic import Json
import pandas as pd
from backend.src.services.data_set_manager import DataSetDataBaseManager
from backend.src.utils.json_dataframe import JsonDataFrame
from backend.src.services.model_trainer import ModelTrainer
from backend.src.services.model_db_manager import ModelDataBaseManager



class DataBaseOrchestrator:
    """
    Classe responsable de la coordination entre la base de données, 
    la transformation des données et l’entraînement des modèles.
    """
    def __init__(self):
        pass

    def add_new_data(self, new_data: str) -> None:
        """
        Ajoute de nouvelles données à la base, déclenche un réentraînement 
        du modèle si le dataset est suffisamment grand, 
        et retourne un résumé JSON pour le front-end."""
        try:
            data_frame:pd.DataFrame = JsonDataFrame().json_to_dataframe(new_data)
            DataSetDataBaseManager().add_to_dataset_database(data_frame)
            result = {
                "status": "success",
                "message": f"{data_frame.shape[0]} lignes ajoutées à la base de données.",
                "rows_added": int(data_frame.shape[0]),
                "model_retrained": False,
            }
            if data_frame.shape[0] > 100:
                latest_data_set: pd.DataFrame = DataSetDataBaseManager().get_latest_dataset()

                features = ["pl_orbper", "pl_rade", "pl_tranmid", "st_teff"]
                X_train = latest_data_set.drop([])
                Y_train = latest_data_set["target"]

                latest_model = ModelDataBaseManager().get_latest_model()
                ModelTrainer().train(latest_model, X_train, Y_train)

                result["model_retrained"] = True
                result["message"] += " Nouveau modèle entraîné avec succès."

            return result

        except Exception as e:
            # En cas d'erreur, retour JSON propre
            return {
                "status": "error",
                "message": f"Erreur lors de l’ajout des données : {str(e)}",
                "rows_added": 0,
                "model_retrained": False,
            }
