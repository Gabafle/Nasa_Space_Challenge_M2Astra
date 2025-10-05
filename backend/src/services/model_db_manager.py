import json
import os
import threading
from datetime import datetime
from typing import Any, Dict
import xgboost as xgb

from backend.src.services.model_trainer import ModelTrainer


class ModelDataBaseManager:
    def __init__(self):
        self.path ="backend/src/data/json_data/models_json.json"

    def _read_db(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_db(self, data: Dict[str, Any]):
        with self.lock, open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def _get_len_data_base(self) -> int:
        return len(self._read_db())
    
    def get_latest_model(self):
        json = self._read_db()
        link = json["file_path"]
        model =        
    
    def add_model(self,model, name: str) -> None:
        
        file_path = "backend/src/data/models_data_base"
        last_model_number = self._get_len_data_base() + 1
        file_path = model.save_model(file_path + "/model"+ str(last_model_number))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_model = {}
        new_model["author_name"] = name
        new_model["timestamp"] = timestamp
        new_model["model_path"] = file_path
        new_model[""]
        
        
        self._write_db(new_model)
        
        
        
        

    def get_latest_model(self):
        # return le model. Lis dans le json et load le  parametre du latest model.
        return


    