import os
import sys

import pandas as pd
import pymongo
from dotenv import load_dotenv
from sklearn.model_selection import (
    train_test_split,  # type: ignore[reportMissingModuleSource]
)

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not set in the .env file")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def export_collection_as_dataframe(self):
        """Export MongoDB collection data as a pandas DataFrame."""
        try:
            logging.info("Connecting to MongoDB...")
            mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            logging.info("Successfully connected to MongoDB")

            db = mongo_client[self.data_ingestion_config.database_name]
            collection = db[self.data_ingestion_config.collection_name]

            logging.info(
                f"Fetching data from collection: {self.data_ingestion_config.collection_name}"
            )
            data = pd.DataFrame(list(collection.find()))

            if "_id" in data.columns:
                data = data.drop("_id", axis=1)

            data.replace(to_replace="na", value=pd.NA, inplace=True)

            logging.info(f"Successfully fetched data. Total records: {len(data)}")

            return data

        except Exception as e:
            logging.exception("Error while fetching data from MongoDB")
            raise NetworkSecurityException(e, sys) from e

    def export_data_to_feature_store(self, data: pd.DataFrame):
        """Export data to feature store directory."""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            data.to_csv(feature_store_file_path, index=False)
            logging.info(
                f"Data successfully exported to feature store at: {feature_store_file_path}"
            )
            return data
        except Exception as e:
            logging.exception("Error while exporting data to feature store")
            raise NetworkSecurityException(e, sys) from e

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info("Exported train and test file path.")

            return train_set, test_set

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
