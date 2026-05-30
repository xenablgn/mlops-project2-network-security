import os
import sys
import pandas as pd
import pymongo
import certifi

from dotenv import load_dotenv
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not set in the .env file")

CA_FILE = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=CA_FILE
            )

            # Verify connection
            self.mongo_client.admin.command("ping")
            logging.info("Successfully connected to MongoDB")

        except Exception as e:
            logging.exception("Failed to connect to MongoDB")
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        """
        Read CSV file and convert it to a list of dictionaries.
        """
        try:
            data = pd.read_csv(file_path)

            # Reset index if needed
            data.reset_index(drop=True, inplace=True)

            # Convert DataFrame to list of records
            records = data.to_dict(orient="records")

            logging.info(
                f"Successfully converted CSV to JSON records. Total records: {len(records)}"
            )

            return records

        except Exception as e:
            logging.exception("Error while converting CSV to JSON")
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database_name, collection_name):
        """
        Insert records into MongoDB collection.
        """
        try:
            db = self.mongo_client[database_name]
            collection = db[collection_name]

            result = collection.insert_many(records)

            inserted_count = len(result.inserted_ids)

            logging.info(
                f"{inserted_count} records inserted into '{collection_name}'"
            )

            return inserted_count

        except Exception as e:
            logging.exception("Error while inserting data into MongoDB")
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        FILE_PATH = os.path.join(
            os.getcwd(),
            "data",
            "phisingData.csv"
        )

        DATABASE_NAME = "NetworkSecurityDB"
        COLLECTION_NAME = "NetworkData"

        network_data = NetworkDataExtract()

        records = network_data.csv_to_json_converter(FILE_PATH)

        inserted_count = network_data.insert_data_to_mongodb(
            records=records,
            database_name=DATABASE_NAME,
            collection_name=COLLECTION_NAME
        )

        logging.info(f"Successfully inserted {inserted_count} records.")

    except Exception as e:
        logging.exception("Application execution failed")
        raise NetworkSecurityException(e, sys)