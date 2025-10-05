from backend.src.services.data_loader import DataLoader
from backend.src.services.model_db_manager import ModelDataBaseManager
from backend.src.services.model_predictor import ModelPredictor
from backend.src.utils.json_dataframe import JsonDataFrame
import pandas as pd


class PredictionOrchestrator:
    """ Cette classe sera utilisé dans le cas de user basic et de researcher qui veut valider les label: Elle renvoie un disctionnaire / json"""
    def __init__(self):
        pass

    def process_and_predict(self, data):
        # chargement en bytes des données
        df = JsonDataFrame().json_to_dataframe(data)

        #df = pd.DataFrame(data["rows"], columns=data["columns"])
    
        
        # Prédiction
        latest_model = ModelDataBaseManager().get_latest_model()
        predictions  = ModelPredictor().predict(latest_model, df)

        return {"predictions": predictions}