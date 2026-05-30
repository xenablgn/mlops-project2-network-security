import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    TrainingPipelineConfig,
)
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class DataIngestionPipeline:
    def __init__(self) -> None:
        """Initialize data ingestion pipeline with config and component."""
        self.data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        self.data_ingestion = DataIngestion(self.data_ingestion_config)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """Run the full data ingestion process and return the artifact."""
        try:
            data = self.data_ingestion.export_collection_as_dataframe()
            data = self.data_ingestion.export_data_to_feature_store(data)

            logging.info("Initiating train-test split...")
            self.data_ingestion.split_data_as_train_test(data)

            return DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

        except Exception as e:
            logging.exception("Error during data ingestion")
            raise NetworkSecurityException(e, sys) from e
