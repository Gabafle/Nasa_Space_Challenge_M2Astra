from hmac import new
import json
import os
from re import X
import threading
from datetime import datetime
from typing import Any, Dict
from unittest.mock import Base
from backend.src.models.xgboost import XGBoostModel
from backend.src.models.base_model import BaseModel

class ModelDataBaseManager:
    def __init__(self):
        self.path ="backend/src/data/json_data/models_json.json"
        self.target_path = "backend/src/data/models_data_base"

    def _read_db(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_db(self, model) -> None:
        """
        Ajoute un nouvel élément JSON dans la clé 'datasets' du fichier existant.
        Si le fichier n'existe pas encore, il est créé avec la structure { "datasets": [] }.
        """
        db = self._read_db()
        db["models"].append(model)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)

            
    def _get_len_data_base(self) -> int:
        """ DONE """
        return len(self._read_db()["models"])
    
    def get_latest_model(self):
        """ DONE """
        json = self._read_db()
        json_last = json["models"][-1]
        link = json_last["file_path"]
        model_wrapper = XGBoostModel()
        model_wrapper.load_model(link)
        
        
        return model_wrapper
    
    def add_model(self,model, name: str) -> None:
        
        last_model_number = self._get_len_data_base() + 1
        file_path = self.target_path + "/model"+ str(last_model_number)
        print("=================")
        print(model.get_params())
        print("=================")
        model.save_model(file_path)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(file_path)
        new_model = {}
        new_model["author_name"] = name
        new_model["created_at"] = timestamp
        new_model["file_path"] = file_path
        new_model["model_name"] = model.__class__.__name__
        new_model["model_id"] = last_model_number

        self._write_db(new_model)



if __name__ == "__main__":
    from xgboost import XGBClassifier
    import numpy as np
    import pandas as pd

    print("=== 🔍 Test du ModelDataBaseManager ===")

    # Création d’un modèle factice XGBoost
    X_train = np.random.rand(20, 4)
    y_train = np.random.randint(0, 2, 20)
    model = XGBClassifier(n_estimators=10, max_depth=3, learning_rate=0.1)
    model.fit(X_train, y_train)

    # Instanciation du manager
    manager = ModelDataBaseManager()


    # Création de la structure JSON si absente
    if not os.path.exists(manager.path):
        with open(manager.path, "w", encoding="utf-8") as f:
            json.dump({"models": []}, f, indent=2, ensure_ascii=False)

    # Ajout du modèle
    print("➡️ Ajout du modèle dans la base...")
    manager.add_model(model, name="Félix Bos")

    # Vérifie le contenu du fichier JSON
    print("✅ Contenu actuel de la base JSON :")
    with open(manager.path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
    latest_model  = manager.get_latest_model()
    print(latest_model.predict(X_train))

    print("=== ✅ Test terminé ===")