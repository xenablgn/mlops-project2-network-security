import sys

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from networksecurity.pipeline.data_transformation_pipeline import (
    DataTransformationPipeline,
)
from networksecurity.pipeline.data_validation_pipeline import DataValidationPipeline

STAGE_NAME = "Data Ingestion Stage"

try:
    logging.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
    pipeline = DataIngestionPipeline()
    data_ingestion_artifact = pipeline.intiate_data_ingestion()
    logging.info(f"Train file path: {data_ingestion_artifact.train_file_path}")
    logging.info(f"Test file path: {data_ingestion_artifact.test_file_path}")
    logging.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logging.exception("Error during data ingestion")
    raise NetworkSecurityException(e, sys) from e


STAGE_NAME = "Data Validation Stage"
try:
    logging.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
    pipeline = DataValidationPipeline(data_ingestion_artifact)
    data_validation_artifact = pipeline.initiate_data_validation()
    logging.info(f"Data Validation Artifact: {data_validation_artifact}")
    logging.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logging.exception("Error during data validation")
    raise NetworkSecurityException(e, sys) from e


STAGE_NAME = "Data Transformation Stage"
try:
    logging.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
    pipeline = DataTransformationPipeline(data_validation_artifact)
    data_transformation_artifact = pipeline.initiate_data_transformation()
    logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
    logging.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logging.exception("Error during data transformation")
    raise NetworkSecurityException(e, sys) from e
