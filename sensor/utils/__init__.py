import pandas as pd
import numpy as np
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import os,sys
import yaml
import dill

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        # Extracting all the records from mongoDB collection converting it into a list and creating a dataframe out of it.
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")

        # Dropping "_id" column from dataframe if exists.
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")

        # Returning dataframe
        return df
    except Exception as e:
        raise SensorException(e, sys)

def write_yaml_file(file_path,data:dict):
    """
    Description: This function will generate a data validation report as yaml file.
    =========================================================
    Params:
    file_path: file path to store the report
    data: Dictionary conaining data validation checks in key value pair
    """
    try:
        # creating "data_ingestion" directory within "artifact".
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)

        # Write all the data collected in "validation_error" dict into yaml file.
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise SensorException(e, sys)

def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    """
    Description: This function will convert independent features value as float.
    =========================================================
    Params:
    df: dataframe
    exclude_columns: Target column
    """
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype('float')
        return df
    except Exception as e:
        raise e


def save_object(file_path: str, obj: object) -> None:
    """
    Description: This function will store models/objects in pickle file format.
    """
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e


def load_object(file_path: str, ) -> object:
    """
    Description: This function will load models/objects from pickle file.
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Description: Save numpy array data to file
    ============================================
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    Description: load numpy array data from file
    =============================================
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e