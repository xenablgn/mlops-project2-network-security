import logging
import os
from pathlib import Path

project_name = "networksecurity"

list_of_files = [
    ".github/workflows/main.yml",
    "network_data/",
    "research/research.ipynb",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "Taskfile.yaml",
    "Dockerfile",
    ".pre-commit-config.yaml",
    "pyproject.toml",
    "main.py",
    "Dockerfile",
    "setup.py",
    "templates/index.html",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/cloud/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/exceptions/__init__.py",
    f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/logging/logging.log",
    f"src/{project_name}/pipeline/__init__.py",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if filename and (not os.path.exists(filepath) or os.path.getsize(filepath) == 0):
        with open(file=filepath, mode="w") as f:
            pass
        logging.info(f"Creating file: {filepath}")
    elif filename:
        logging.info(f"File already exists: {filepath}")
