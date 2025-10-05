import pandas as pd
import json

class JsonDataFrame:
    """ Cette classe implémente les fonction necessaire pour passer de l'un à l'autre. Avec le json utilisé dans le frontend"""
    def __init__(self):
        self.feat_cols = [
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

        self.score_cols = ["softmax_class_1", "softmax_class_2", "softmax_class_3"]
        self.score_cols_front = ["softmax_class_1", "softmax_class_2", "softmax_class_3"]
        
        self.target_col = "target"
        self.target_col_front = "vrai label"


    
    def json_to_dataframe(self, json_str: str) -> pd.DataFrame:
        """ Respectez le format du front pour le json """
        # do the opposite of dataframe_to_json
        if isinstance(json_str, str): data = json.loads(json_str)
        else : data = json_str  # assume it's already a list of dicts
        
        # Prepare a list to collect the DataFrame rows
        rows = []
        
        for entry in data:
            row = {}
            row["id"] = entry["id"]
            
            # Extract feature values
            for feat in self.feat_cols:
                row[feat] = entry["vals"].get(feat, None)  # Use None if key is missing

            # Extract SHAP values, if they exist
            for feat in self.feat_cols:
                shap_col = f"{feat}_SHAP"
                if "shapley" in entry and feat in entry["shapley"]:
                    row[shap_col] = entry["shapley"][feat]

            # Extract target value, if it exists
            if self.target_col_front in entry:
                row[self.target_col] = entry[self.target_col_front]

            # Extract score values, if they exist
            for score_f, score_b in zip(self.score_cols_front, self.score_cols):
                if score_f in entry:
                    row[score_b] = entry[score_f]
            
            rows.append(row)
        
        # Convert the list of rows into a DataFrame
        df = pd.DataFrame(rows)
        df[self.feat_cols] = df[self.feat_cols].astype(float)
        return df


    def dataframe_to_json(self, df: pd.DataFrame) -> str:
        """ doit respecter les souhait du front voir discord"""
        result = []

        assert all(col in df.columns for col in (self.feat_cols+['id'])), f"df is missing one of the following cols: {self.feat_cols+['id']}"

        has_score = set(self.score_cols).issubset(df.columns)
        has_target = set(self.target_col).issubset(df.columns)
        has_shap = set([col + '_SHAP' for col in self.feat_cols]).issubset(df.columns)
        
        # Iterate over each row in the dataframe
        for _, row in df.iterrows():
            features = {}
            shapley_values = {}
            
            # For each feature column (exclude 'id' column or any non-feature columns)
            for feat in self.feat_cols:
                features[feat] = row[feat]  # Convert to int
                if has_shap:
                    shap_col = f"{feat}_SHAP"
                    shapley_values[feat] = row[shap_col]  # Convert to int
            
            # Create the JSON structure for the current row
            row_json = {
                "id": row["id"],
                "vals": features
            }
            if has_shap: row_json["shapley"] = shapley_values
            if has_target: row_json[self.target_col_front] = row[self.target_col]
            if has_score:
                for score_f, score_b in zip(self.score_cols_front, self.score_cols):
                    row_json[score_f] = float(row[score_b])
            
            result.append(row_json)

        # print(f"{df.columns=}")
        # print(f"{set(self.score_cols).issubset(df.columns)=}")
        # print(f"{set(self.target_col).issubset(df.columns)=}")
        # print(f"{set([col + '_SHAP' for col in self.feat_cols]).issubset(df.columns)=}")
        # print(f"{row_json=}")
        # print(f"{has_score=}")
        # print(f"{has_target=}")
        # print(f"{has_shap=}")
        
        return json.dumps({"dataframe": result}, indent=4)
