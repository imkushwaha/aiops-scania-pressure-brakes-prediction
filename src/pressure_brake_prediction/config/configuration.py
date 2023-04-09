from pressure_brake_prediction.constants import *
from pressure_brake_prediction.utils import read_yaml, create_directories
from pressure_brake_prediction.entity import (DataIngestionConfig, 
                                              DataTransformationConfig)


class ConfigurationManager:
    def __init__(
            self, 
            config_filepath = CONFIG_FILE_PATH, 
            params_filepath = PARAM_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_data_file=config.source_data_file,
            local_data_file=config.local_data_file, 
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir, 
            raw_train_data = config.raw_train_data, 
            raw_test_data = config.raw_test_data,
            train_data = config.train_data, 
            test_data = config.test_data,
            preprocessor_obj_file_path = config.preprocessor_obj_file_path,
            target_column = config.target_column
        )

        return data_transformation_config