from xgboost import XGBClassifier
from backend.src.models.xgboost import XGBoostModel
from backend.src.services.data_set_manager import DataSetDataBaseManager
from backend.src.services.model_db_manager import ModelDataBaseManager

df = DataSetDataBaseManager().get_latest_dataset()



X_train, y_train = df.drop(["target", "ID"], axis = 1),df["target"]

xgb_model = XGBoostModel()
xgb_model.set_params()

print(xgb_model.get_params())

xgb_model.train(X_train, y_train)


ModelDataBaseManager().add_model(xgb_model, name="Félix Bos")


print("-----COUUUUUUU----")
print(ModelDataBaseManager().get_latest_model().get_params())




