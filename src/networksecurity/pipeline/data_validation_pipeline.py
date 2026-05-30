import os
import sys

from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from networksecurity.entity.config_entity import (
    DataValidationConfig,
    TrainingPipelineConfig,
)
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class DataValidationPipeline:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact) -> None:
        """Initialize data validation pipeline with config and component."""
        self.data_validation_config = DataValidationConfig(TrainingPipelineConfig())
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation = DataValidation(
            data_validation_config=self.data_validation_config,
        )

    def initiate_data_validation(
        self,
    ) -> DataValidationArtifact:
        """Run the full data validation process and return the artifact."""
        try:
            logging.info("Starting data validation")

            train_df = self.data_validation.read_data(
                self.data_ingestion_artifact.train_file_path
            )

            test_df = self.data_validation.read_data(
                self.data_ingestion_artifact.test_file_path
            )

            validation_passed = True

            # Validate column count
            if not self.data_validation.validate_number_of_columns(train_df):
                validation_passed = False

            if not self.data_validation.validate_number_of_columns(test_df):
                validation_passed = False

            # Validate schema
            if not self.data_validation.detect_column_names(train_df):
                validation_passed = False

            if not self.data_validation.detect_column_names(test_df):
                validation_passed = False

            # Stop validation if schema checks fail
            if not validation_passed:
                raise ValueError(
                    "Data validation failed due to "
                    "column mismatch or missing columns."
                )

            drift_detected = self.data_validation.validate_dataset_drift(
                base_df=train_df,
                current_df=test_df,
            )

            logging.info(
                f"Data validation completed. " f"Drift detected: {drift_detected}"
            )

            valid_train_dir = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )

            if valid_train_dir:
                os.makedirs(
                    valid_train_dir,
                    exist_ok=True,
                )

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
            )

            return DataValidationArtifact(
                validation_status=validation_passed,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
