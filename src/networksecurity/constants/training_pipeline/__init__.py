import os
import sys
import numpy as np
import pandas as pd

"""
Definning all the constants related to training pipeline
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "artifacts"
FILE_NAME = "phishingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

"""
Data Ingestion related constants start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DATABASE_NAME = "NetworkSecurityDB"
DATA_INGESTION_FILE_NAME = "phishingData.csv"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2
DATA_INGESTION_RANDOM_STATE = 42
