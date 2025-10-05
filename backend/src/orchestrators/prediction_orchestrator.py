import json
from backend.src.services.data_loader import DataLoader
from backend.src.services.model_db_manager import ModelDataBaseManager
from backend.src.services.model_predictor import ModelPredictor
from backend.src.utils.json_dataframe import JsonDataFrame
import pandas as pd

def convert_front_json_to_backend_format(front_json: dict) -> list:
    """
    Convertit un JSON de la forme {"columns": [...], "rows": [...]} 
    en liste de dictionnaires compatible avec la fonction json_to_dataframe().

    Exemple d'entrée :
    {
        "columns": ["pl_orbper", "pl_rade", ..., "target", "ID"],
        "rows": [{"pl_orbper": "...", "pl_rade": "...", "target": "...", "ID": "..."}]
    }

    Exemple de sortie :
    [
        {
            "id": "K00752.01",
            "vals": {"pl_orbper": "...", "pl_rade": "...", ...},
            "shapley": {},
            "targetFront": "2"
        },
        ...
    ]
    """
    converted = []
    columns = front_json.get("columns", [])
    rows = front_json.get("rows", [])

    for row in rows:
        # Construction du dictionnaire compatible avec ton backend
        entry = {
            "id": row.get("ID"),
            "vals": {k: row[k] for k in columns if k not in ["target", "ID"]},
            "shapley": {},  # laissé vide par défaut
            "targetFront": row.get("target")
        }
        converted.append(entry)

    return converted


class PredictionOrchestrator:
    """ Cette classe sera utilisé dans le cas de user basic et de researcher qui veut valider les label: Elle renvoie un disctionnaire / json"""
    def __init__(self):
        pass

    def process_and_predict(self, data):
        # chargement en bytes des données
        
        json_df = convert_front_json_to_backend_format(data)
        df = JsonDataFrame().json_to_dataframe(json_df)

        #df = pd.DataFrame(data["rows"], columns=data["columns"])
    
        
        # Prédiction
        latest_model = ModelDataBaseManager().get_latest_model()
        predictions  = ModelPredictor().predict(latest_model, df)

        return predictions