import pandas as pd

class DataSetDataBaseManager:
    def __init__(self):
        pass
    
    def get_latest_dataset(self) -> pd.DataFrame:
        """ Search with json file data.json. based on date."""
    
        # get the link of the latest dataset from json mapper.
       
        latest_data_set_link: str = ""    # TODO
        
        latest_data_frame = pd.read_csv(latest_data_set_link, sep = ";")
        return latest_data_frame
    

    def add_to_dataset_database(self, author:str, email_author: str, new_data :pd.DataFrame) -> None:
        """ Chercher dans le json le dernier data set. Modifier concaténant le  data frame."""
        # get latest dataframe as pandas
        latest_data_frame = self.get_latest_dataset()
        
        # concerver le latest
        temp = latest_data_frame
        
        # concénation des deux df 
        latest_data_frame = pd.concat(latest_data_frame, new_data, ignore_index=True)
        
        # Add the temp / update json mapper
        pass
    
    def get_history(self) -> list[pd.DataFrame]:
        return self.history_dataset
    
    def get_history_as_json(self) -> str:
        pass
    
    def get_data_set_from_json(self) -> pd.DataFrame:
        pass
    
    
    