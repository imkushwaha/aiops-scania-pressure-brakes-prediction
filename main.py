from pressure_brake_prediction.pipeline.stage_01_data_ingestion import DataIngestionTrainningPipeline
from pressure_brake_prediction import logger

stage_name = "Data Ingestion stage"

try:
    logger.info(f">>>>> stage {stage_name} started <<<<<")
    data_ingestion = DataIngestionTrainningPipeline()
    data_ingestion.main()
    logger.info(f">>>>> Stage {stage_name} completed <<<<<")

except Exception as e:
    logger.exception(e)
    raise e