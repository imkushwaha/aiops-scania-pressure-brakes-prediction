from pressure_brake_prediction.pipeline.stage_01_data_ingestion import DataIngestionTrainningPipeline
from pressure_brake_prediction.pipeline.stage_02_data_transformation import DataTransformationTrainningPipeline
from pressure_brake_prediction.logger import logging
import sys

stage_name = "Data Ingestion stage"

try:
    logging.info(f">>>>> stage {stage_name} started <<<<<")
    data_ingestion = DataIngestionTrainningPipeline()
    data_ingestion.main()
    logging.info(f">>>>> Stage {stage_name} completed <<<<<")

except Exception as e:
    logging.exception(e)
    raise e


stage_name = "Data Transformation stage"
try:
    logging.info(f">>>>> Stage {stage_name} started <<<<<")
    data_transformation = DataTransformationTrainningPipeline()
    data_transformation.main()
    logging.info(f">>>>> Stage {stage_name} completed. <<<<<")

except Exception as e:
    logging.exception(e, sys)
    raise e