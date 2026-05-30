
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import sys


class DataIngestionPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_ingestion = DataIngestion(self.data_ingestion_config)

    def intiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data = self.data_ingestion.export_collection_as_dataframe()
            data = self.data_ingestion.export_data_to_feature_store(data)

            logging.info("Initiating train-test split...")
            train_data, test_data = self.data_ingestion.split_data_as_train_test(data)

            return DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

        except Exception as e:
            logging.exception("Error during data ingestion")
            raise NetworkSecurityException(e, sys)
