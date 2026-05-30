import os
import pickle
import sys

import numpy as np
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError

from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """Read a YAML file and return its contents as a dictionary."""
    try:
        with open(file_path) as yaml_file:
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


def save_numpy_array(file_path: str, array: np.ndarray):
    """Save a NumPy array to a file."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
        logging.info(f"Successfully saved NumPy array to {file_path}")
    except Exception as e:
        logging.exception(f"Error saving NumPy array to {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e


def load_numpy_array(file_path: str) -> np.ndarray:
    """Load a NumPy array from a file."""
    try:
        with open(file_path, "rb") as file:
            array = np.load(file)
        logging.info(f"Successfully loaded NumPy array from {file_path}")
        return array
    except Exception as e:
        logging.exception(f"Error loading NumPy array from {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: str, obj: object):
    """Save a Python object to a file using pickle."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info(f"Successfully saved object to {file_path}")
    except Exception as e:
        logging.exception(f"Error saving object to {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e
