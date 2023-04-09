from pressure_brake_prediction.config.configuration import ConfigurationManager
from pressure_brake_prediction.components.data_transformation_and_split_data import DataTransformation
from pressure_brake_prediction.exception import CustomException
from pressure_brake_prediction.logger import logging
import sys

class DataTransformationTrainningPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(data_transformation_config)
            data_transformation.initiate_transformer()
        except Exception as e:
            raise e