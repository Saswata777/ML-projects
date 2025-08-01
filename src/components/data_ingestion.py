import os
import sys # used for custom exception
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.exception import CustomException
from src.logger import logging




import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig



'''
In Python, @dataclass is a decorator provided by the dataclasses module
(available from Python 3.7+). It is used to automatically generate special methods for 
classes like __init__(), __repr__(), __eq__(), and more — so you don’t have to write
boilerplate code manually.
'''

'''
✅ DataIngestionConfig class
This class holds file paths used in the data ingestion phase of an ML 
pipeline — typically where you:

Load the raw dataset
Split it into train and test
Save those files

'''

@dataclass
class DataIngestionConfig: 
    """
    Configuration class that holds file paths for raw, train, and test data.
    These will be saved in the 'artifacts' directory.
    """
    train_data_path: str = os.path.join('artifacts', "train.csv") # train.csv file get store in artifacts
    test_data_path: str = os.path.join('artifacts', "test.csv") # test.csv file get store in artifacts
    raw_data_path: str = os.path.join('artifacts', "data.csv") # data.csv file get store in artifacts
    
    
    
# -------------------------
# 🔁 Data Ingestion Logic
# -------------------------
    
class DataIngestion:
    '''
        This class handles the entire data ingestion process:
        - Reads the raw dataset
        - Saves a backup copy
        - Splits the dataset into training and testing sets
        - Saves the split data into specified paths
    '''
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Step 1: Load raw data
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info("Raw dataset loaded successfully into a DataFrame.")

            # Step 2: Ensure the target directory exists
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Step 3: Save raw data as backup
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved to: %s", self.ingestion_config.raw_data_path)

            # Step 4: Split data into train and test sets
            logging.info("Initiating train-test split.")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Step 5: Save train and test datasets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Train and test datasets saved successfully.")

            # Step 6: Return file paths
            logging.info("Data ingestion completed successfully.")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            logging.error("Exception occurred during data ingestion: %s", str(e))
            raise CustomException(e, sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    # obj.initiate_data_ingestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_= data_transformation.initiate_data_transformation(train_data,test_data)

#     modeltrainer=ModelTrainer()
#     print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
    
    