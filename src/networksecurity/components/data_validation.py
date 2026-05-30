import os
import sys

import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.common import (
    read_yaml_file,
    write_yaml_file,
)


class DataValidation:
    def __init__(
        self,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_validation_config = data_validation_config
            self.schema = read_yaml_file(self.data_validation_config.schema_file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def validate_number_of_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> bool:
        expected_columns = len(self.schema["columns"])
        actual_columns = dataframe.shape[1]

        if actual_columns != expected_columns:
            logging.error(
                f"Column count mismatch. "
                f"Expected={expected_columns}, "
                f"Actual={actual_columns}"
            )
            return False

        return True

    def detect_column_names(
        self,
        dataframe: pd.DataFrame,
    ) -> bool:
        expected_columns = set(list(col.keys())[0] for col in self.schema["columns"])
        actual_columns = set(dataframe.columns)

        missing_columns = expected_columns - actual_columns

        if missing_columns:
            logging.error(f"Missing columns found: {missing_columns}")
            return False

        return True

    def validate_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05,
    ) -> bool:
        try:
            drift_detected = False
            report = {}

            for column in base_df.columns:
                if column not in current_df.columns:
                    report[column] = {"missing_in_current_dataset": True}
                    drift_detected = True
                    continue

                if not pd.api.types.is_numeric_dtype(base_df[column]):
                    continue

                base_series = base_df[column].dropna()
                current_series = current_df[column].dropna()

                if len(base_series) == 0 or len(current_series) == 0:
                    continue

                _, p_value = ks_2samp(
                    base_series,
                    current_series,
                )

                drift_status = bool(p_value < threshold)

                report[column] = {
                    "p_value": float(p_value),
                    "drifted": drift_status,
                }

                if drift_status:
                    drift_detected = True

            report_path = self.data_validation_config.drift_report_file_path

            report_dir = os.path.dirname(report_path)

            if report_dir:
                os.makedirs(
                    report_dir,
                    exist_ok=True,
                )

            write_yaml_file(
                file_path=report_path,
                data=report,
            )

            return drift_detected

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
