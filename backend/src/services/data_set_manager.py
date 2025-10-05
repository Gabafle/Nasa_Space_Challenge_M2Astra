import datetime
from typing import Any, Dict
import pandas as pd
import os
import json

class DataSetDataBaseManager:
    def __init__(self):
        self.path ="backend/src/data/json_data/datasets_json.json"
        self.target_path = "backend/src/data/datasets"

    def _read_db(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_db(self, dataframe_as_json) -> None:
        """
        Ajoute un nouvel élément JSON dans la clé 'datasets' du fichier existant.
        Si le fichier n'existe pas encore, il est créé avec la structure { "datasets": [] }.
        """
        db = self._read_db()
        db["datasets"].append(dataframe_as_json)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
            
    def _get_len_data_base(self) -> int:
        return len(self._read_db())
    
    def get_latest_dataset(self) -> pd.DataFrame:
        """ Search with json file data.json. based on date."""
        # get the link of the latest dataset from json mapper.
        """ DONE """
        json = self._read_db()
        json_last = json["datasets"][-1]
        link = json_last["file_path"]
        latest_data_frame = pd.read_csv(link, sep = ",")
        return latest_data_frame 
    

    def add_to_dataset_database(self, author:str, email_author: str, new_data :pd.DataFrame) -> None:
        """ Chercher dans le json le dernier data set. Modifier concaténant le  data frame."""
        # get latest dataframe as pandas
        latest_data_frame = self.get_latest_dataset()
        
        # concerver le latest
        temp = latest_data_frame
        
        # concénation des deux df 
        latest_data_frame = pd.concat(latest_data_frame, new_data, ignore_index=True)
        
        new_data_set = {}
        new_data_set["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data_set["author_name"] = author
        

        
        # Add the temp / update json mapper
        pass


if __name__ == "__main__":
    import numpy as np

    print("=== 🔍 Test du DataSetDataBaseManager ===")

    # Instanciation du gestionnaire
    manager = DataSetDataBaseManager()

    df_latest = manager.get_latest_dataset()
    print(df_latest)
    print("\n=== ✅ Test terminé ===")
