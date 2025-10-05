from backend.src.services.data_loader import DataLoader
import pandas as pd


class PredictionOrchestrator:
    """ Cette classe sera utilisé dans le cas de user basic et de researcher qui veut valider les label: Elle renvoie un disctionnaire / json"""
    def __init__(self):
        pass

    def process_and_predict(self, file_content: bytes, filename: str):
        # chargement en bytes des données
        load_result = DataLoader().load_bytes(file_content, filename)
        if not load_result.ok:
            # Cette erreur doit etre géré coté front end
            return {"error": "Data loading failed", "details": load_result.to_dict()}

        # Convertir les données en DataFrame
        df = pd.DataFrame(load_result.rows)
        
        
        predictions = self.model.predict(df)

        return {"predictions": predictions}


