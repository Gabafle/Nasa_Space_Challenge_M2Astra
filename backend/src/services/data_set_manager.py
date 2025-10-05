import pandas as pd

class DataSetDataBaseManager:
    def __init__(self,):
        # On initialise avec notre data frame. Cela évoluera dans le temps
        self.latest_dataset = None
        self.history_dataset = []

    def get_latest_dataset(self) -> pd.DataFrame:
        return self.latest_dataset

    def add_to_dataset_database(self, new_data: pd.DataFrame) -> None:
        """ Conctène new data avec self.latest_dataset. Penser à bien verifier les bonne valeur de colonne ... """
        pass
    
    def get_history(self) -> list[pd.DataFrame]:
        return self.history_dataset
    
    def get_history_as_json(self) -> str:
        # return un json avec le chercheur qui a ajouté les données. Le lien vers src.data.datasets et la date de creation
        pass
    
    def get_data_set_from_json(self) -> pd.DataFrame:
        pass
    
    
    