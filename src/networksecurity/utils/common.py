import pandas as pd
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import dill
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError


def read_yaml_file(file_path: str) -> dict:
    """Read a YAML file and return its contents as a dictionary."""
    try:
        with open(file_path, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"Successfully read YAML file at {file_path}")
            return ConfigBox(content)  # Return as ConfigBox for attribute-style access
    except BoxValueError as e:
        logging.exception(f"Error parsing YAML file at {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e


def write_yaml_file(file_path: str, data: dict):
    """Write a dictionary to a YAML file."""
    try:
        with open(file_path, "w") as yaml_file:
            yaml.safe_dump(data, yaml_file)
            logging.info(f"Successfully wrote YAML file at {file_path}")
    except Exception as e:
        logging.exception(f"Error writing YAML file at {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e
