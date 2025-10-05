import json
import time
import joblib
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, learning_curve
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)


class ModelEvaluator:
    """
    Classe de gestion complète d'un modèle sklearn :
      - Entraînement (avec cross-validation détaillée)
      - Évaluation train/test
      - Export JSON structuré
      - Sauvegarde modèle
      - Réglage dynamique des hyperparamètres
    """

    def __init__(self, model, X, y = None, class_labels=None, feature_names=None, test_size=0.25, random_state=42):
        self.model = model
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.class_labels = class_labels if class_labels is not None else np.unique(y)
        self.feature_names = feature_names if feature_names is not None else [f"feature_{i}" for i in range(X.shape[1])]
        self.report = {}

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state
        )

    def predict(self, X):
        """
        Retourne un JSON contenant :
          - les features d'entrée
          - la classe prédite
          - les probabilités associées
        """
        y_pred = self.model.predict(X)
        y_proba = self.model.predict_proba(X)

        predictions = []
        for i in range(len(X)):
            # Dictionnaire des features
            features = {
                self.feature_names[j]: float(X[i][j])
                for j in range(len(self.feature_names))
            }
            # Dictionnaire des probabilités
            probas = {
                str(self.class_labels[k]): round(float(y_proba[i][k]), 4)
                for k in range(len(self.class_labels))
            }

            predictions.append({
                "input_features": features,
                "predicted_class": str(y_pred[i]),
                "class_probabilities": probas
            })

        result = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model_name": type(self.model).__name__,
            "num_samples": len(X),
            "num_features": len(self.feature_names),
            "predictions": predictions
        }

        return json.dumps(result, indent=4, ensure_ascii=False)


    def train(self, cv=5):
        kf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)
        folds = []
        accuracies, fit_times, score_times = [], [], []

        for i, (train_idx, val_idx) in enumerate(kf.split(self.X_train, self.y_train)):
            X_tr, X_val = self.X_train[train_idx], self.X_train[val_idx]
            y_tr, y_val = self.y_train[train_idx], self.y_train[val_idx]

            start_fit = time.time()
            self.model.fit(X_tr, y_tr)
            fit_time = round(time.time() - start_fit, 3)

            start_score = time.time()
            y_pred = self.model.predict(X_val)
            score_time = round(time.time() - start_score, 3)

            y_prob = self.model.predict_proba(X_val)
            metrics = self._compute_metrics(y_val, y_pred, y_prob)

            folds.append({
                "fold": i + 1,
                "train_size": len(X_tr),
                "val_size": len(X_val),
                "metrics": metrics,
                "fit_time_sec": fit_time,
                "score_time_sec": score_time
            })

            accuracies.append(metrics["accuracy"])
            fit_times.append(fit_time)
            score_times.append(score_time)

        self.model.fit(self.X_train, self.y_train)

        self.training_info = {
            "fit_time_sec": round(np.mean(fit_times), 3),
            "predict_time_sec": round(np.mean(score_times), 3),
            "cross_validation_folds": cv,
            "cross_val_score_mean": round(np.mean(accuracies), 4),
            "cross_val_score_std": round(np.std(accuracies), 4)
        }

        self.cross_validation_results = {
            "folds": folds,
            "summary": {
                "mean_accuracy": round(np.mean(accuracies), 4),
                "std_accuracy": round(np.std(accuracies), 4),
                "mean_fit_time": round(np.mean(fit_times), 3),
                "mean_score_time": round(np.mean(score_times), 3)
            }
        }
        return self.model
    
    def evaluate(self):
        y_pred_train = self.model.predict(self.X_train)
        y_pred_test = self.model.predict(self.X_test)
        y_prob_test = self.model.predict_proba(self.X_test)

        train_metrics = self._compute_metrics(self.y_train, y_pred_train)
        test_metrics = self._compute_metrics(self.y_test, y_pred_test, y_prob_test)

        cm = confusion_matrix(self.y_test, y_pred_test)
        cm_norm = (cm / cm.sum(axis=1, keepdims=True)).round(3)

        train_sizes, train_scores, test_scores = learning_curve(
            self.model, self.X_train, self.y_train,
            cv=5, scoring="accuracy", train_sizes=np.linspace(0.1, 1.0, 7), n_jobs=-1
        )

        learning_curve_info = {
            "train_sizes": train_sizes.tolist(),
            "train_scores_mean": np.mean(train_scores, axis=1).round(4).tolist(),
            "train_scores_std": np.std(train_scores, axis=1).round(4).tolist(),
            "test_scores_mean": np.mean(test_scores, axis=1).round(4).tolist(),
            "test_scores_std": np.std(test_scores, axis=1).round(4).tolist()
        }

        feat_importance = None
        if hasattr(self.model, "feature_importances"):
            feat_importance = [
                {"name": str(i), "importance": round(imp, 4)}
                for i, imp in enumerate(self.model.feature_importances)
            ]
            feat_importance = sorted(feat_importance, key=lambda x: x["importance"], reverse=True)[:10]

        self.report = {
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model_name": type(self.model).__name__,
                "framework": "scikit-learn",
                "model_version": "1.0.0",
                "train_dataset_size": len(self.X_train),
                "test_dataset_size": len(self.X_test),
                "num_features": self.X_train.shape[1],
                "num_classes": len(np.unique(self.y_train)),
                "target_names": self.class_labels.tolist()
            },
            "training_info": self.training_info,
            "cross_validation_results": self.cross_validation_results,
            "train_metrics": train_metrics,
            "test_metrics": test_metrics,
            "confusion_matrix": {
                "matrix": cm.tolist(),
                "labels": self.class_labels.tolist(),
                "normalized": cm_norm.tolist()
            },
            "learning_curve": learning_curve_info,
            "feature_importance": {
                "top_features": feat_importance,
                "method": "Gini importance" if feat_importance else None
            }
        }

        return self.report
    
    
    def save_model(self, path="trained_model.joblib"):
        joblib.dump(self.model, path)
        return path

    def export_json(self, path=None, indent=4):
        json_str = json.dumps(self.report, indent=indent)
        if path:
            with open(path, "w") as f:
                f.write(json_str)
        return json_str

    def _compute_metrics(self, y_true, y_pred, y_prob=None):
        metrics = {
            "accuracy": round(accuracy_score(y_true, y_pred), 4),
            "precision": round(precision_score(y_true, y_pred, average="micro"), 4),
            "recall": round(recall_score(y_true, y_pred, average="micro"), 4),
            "f1": round(f1_score(y_true, y_pred, average="micro"), 4),
        }
        return metrics
    

