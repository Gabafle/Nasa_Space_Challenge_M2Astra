import json
import numpy as np
import pandas as pd
from backend.src.utils.json_dataframe import JsonDataFrame


class ModelPredictor:
    def __init__(self):
        
        # fixe.
        self.class_labels = [ "False Positive", "Confirmed", "Candidate"]
        self.feature_names = None

    def predict(self, model, X: pd.DataFrame) -> str:
        """Retourne un JSON détaillé pour chaque observation (planète)."""
        output_df = model.predict(X)
        
        
        
        # TODO remove TESTPRINT check col names
        print("Columns in output_df in ModelPredictor.predict Call:", output_df.columns.tolist())

        print(output_df)
        output_json_str = JsonDataFrame().dataframe_to_json(output_df)

        return output_json_str
