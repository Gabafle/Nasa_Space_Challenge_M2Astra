import json
import os
import threading
from datetime import datetime
from typing import Any, Dict

class ModelDataBaseManager:
    def __init__(self, db_path: str = "models_db.json"):
        self.db_path = db_path
        self.lock = threading.Lock()  # sécurité lecture/écriture concurrente
        self._init_db()

    def _init_db(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump({"latest_model_id": None, "models": {}}, f, indent=2, ensure_ascii=False)

    def _read_db(self) -> Dict[str, Any]:
        with self.lock, open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_db(self, data: Dict[str, Any]):
        with self.lock, open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_model(self, author: str, description: str, score: float, path: str) -> str:
        db = self._read_db()
        model_id = f"model_{len(db['models']) + 1}"
        db["models"][model_id] = {
            "author": author,
            "description": description,
            "score": score,
            "path": path,
            "created_at": datetime.now().isoformat()
        }
        db["latest_model_id"] = model_id
        self._write_db(db)
        return model_id

    def get_latest_model(self) -> Dict[str, Any]:
        db = self._read_db()
        latest_id = db["latest_model_id"]
        if latest_id is None:
            return {}
        return {latest_id: db["models"][latest_id]}

    def get_model_history(self) -> Dict[str, Any]:
        db = self._read_db()
        return db["models"]

    def get_model_history_as_json(self) -> str:
        return json.dumps(self.get_model_history(), indent=2, ensure_ascii=False)


    