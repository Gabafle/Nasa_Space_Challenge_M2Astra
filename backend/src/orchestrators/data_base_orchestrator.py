from pydantic import Json
import pandas as pd
from backend.src.services.data_set_manager import DataSetDataBaseManager
from backend.src.utils.json_dataframe import JsonDataFrame
from backend.src.services.model_trainer import ModelTrainer


class DataBaseOrchestrator:
    """"""
    def __init__(self):
        pass
    
    def add_new_data(self, new_data) -> None:
        # new data : json -> key : ID , columns_name, X, Y.
        
        data_frame = JsonDataFrame().json_to_dataframe(new_data)
        DataSetDataBaseManager().add_to_dataset_database(data_frame)
        if data_frame.shape[0] >  100:
            # should train the latest model
            latest_data_set : pd.DataFrame = DataSetDataBaseManager().get_latest_dataset()
            model_trainer = ModelTrainer()
            model_trainer.train(latest_data_set)
        
    
        