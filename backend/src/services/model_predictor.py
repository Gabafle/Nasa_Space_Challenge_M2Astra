import json
import numpy as np
import pandas as pd

class ModelPredictor:
    def __init__(self):
        
        # fixe.
        self.class_labels = [ "False Positive", "Confirmed", "Candidate"]
        self.feature_names = None

    def predict(self, model, X: pd.DataFrame) -> str:
        """Retourne un JSON détaillé pour chaque observation (planète)."""
        y_pred = model.predict(X)
        y_proba = model.predict_proba(X)
        
        
        y_pred = [self.class_labels[i] for i in y_pred]
        self.feature_names = X.columns.tolist()
        

        # TODO To match the front json. 
        #planets = []
        #for i in range(len(X)):
        #    planet_data = {
        #        "features": {
        #            self.feature_names[j]: float(X[i][j])
        #            for j in range(len(self.feature_names))
        #        },
        #        "predicted_class": str(y_pred[i]),
        #        "class_probabilities": {
        #            str(self.class_labels[k]): round(float(y_proba[i][k]), 4)
        #            for k in range(len(self.class_labels))
        #        }
        #    }
        #   planets.append(planet_data)

        #result = {
        #    "num_samples": len(X),
        #    "predictions": planets,
        #}

        return #json.dumps(result, indent=4, ensure_ascii=False)
