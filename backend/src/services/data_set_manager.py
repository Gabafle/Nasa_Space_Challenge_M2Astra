import pandas as pd

class DataSetDataBaseManager:
    def __init__(self):
        pass
    
    def get_latest_dataset(self) -> pd.DataFrame:
        """ Search with json file data.json. based on date."""
        pass

    def add_to_dataset_database(self, new_data :pd.DataFrame) -> None:
        """ Chercher dans le json le dernier data set. Modifier concaténant le  data frame."""
        pass
    
    def get_history(self) -> list[pd.DataFrame]:
        return self.history_dataset
    
    def get_history_as_json(self) -> str:
        # return un json avec le chercheur qui a ajouté les données. Le lien vers src.data.datasets et la date de creation
        pass
    
    def get_data_set_from_json(self) -> pd.DataFrame:
        pass
    
    
    