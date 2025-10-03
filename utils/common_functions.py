import os
import pandas as pd

from src.logger import get_logger
from src.custom_exception import CustomException
import yaml


logger = get_logger(__name__)   
# I am new how does this upper command work and why is it there? 

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist in the given path.")
            # what does the aove line do? 
        
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {file_path} loaded successfully.")
            return config
        
    except Exception as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException("Failed to read yaml file ", e)
        

def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading the data {e}")
        raise CustomException("Failed to load data" , e)
    