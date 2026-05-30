from networksecurity.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import sys


STAGE_NAME = "Data Ingestion Stage"

try:
    logging.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
    pipeline = DataIngestionPipeline()
    train_test_paths=pipeline.intiate_data_ingestion()
    logging.info(f"Train file path: {train_test_paths.train_file_path}")
    logging.info(f"Test file path: {train_test_paths.test_file_path}")
    logging.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logging.exception(e)




