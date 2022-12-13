import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from datetime import datetime

FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:

    def __init__(self):
        try:
            # Creating "artifact" directory and within that creating a folder with name as timestamp.
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception  as e:
            raise SensorException(e,sys)     


class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="aps"
            self.collection_name="sensor"
            # creating "data_ingestion" directory within "artifact".
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")
            
            # creating "feature_store" directory within "data_ingestion" to store CSV file extracted from MongoDB.
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)

            # creating "dataset" directory within "data_ingestion" to store train and test file created after traintestsplit.
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception  as e:
            raise SensorException(e,sys)     

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise SensorException(e,sys)     

class DataValidationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        # creating "data_validation" directory within "artifact".
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_validation")

        # creating "report.yaml" file inside "data_validation" directory.
        self.report_file_path=os.path.join(self.data_validation_dir, "report.yaml")

        self.missing_threshold:float = 0.7
        self.base_file_path = os.path.join("aps_failure_training_set1.csv")

class DataTransformationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        # creating "data_transformation" directory within "artifact".
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_transformation")

        # creating "transformer.pkl" file inside "data_transformation" directory.
        self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)

        # creating "train.csv" and "test.csv" files inside "transformed" directory. 
        self.transformed_train_path = os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))
        self.transformed_test_path = os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))

        # creating "target_encoder.pkl" file inside "target_encoder" directory.
        self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)

class ModelTrainerConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        # creating "model_trainer" directory within "artifact".
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir , "model_trainer")

        # creating "model.pkl" file inside "model_trainer" directory.
        self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
        
        self.expected_score = 0.7
        self.overfitting_threshold = 0.1

class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = 0.01

class ModelPusherConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        # creating "model_pusher" directory within "artifact".
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir , "model_pusher")

        # creating "saved_models" directory.
        self.saved_model_dir = os.path.join("saved_models")

        self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
        self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
        self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_FILE_NAME)