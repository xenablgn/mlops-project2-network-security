"""
The setup.py is an essential part of packaging and distributing Python projects.
It is used by setuptools (or distutils in older Python versions) to define the
configuration of your project, such as metadata and dependencies.
"""

# Find the __init__.py files by find_packages() and include them in the package distribution
from setuptools import find_packages, setup


def get_requirements(*file_paths: str) -> list[str]:
    """
    Reads the requirements from one or more files and returns them as a list.

    Args:
        *file_paths (str): The paths to the requirements files.
    Returns:
        List[str]: A list of requirements.
    """
    requirements = []
    for file_path in file_paths:
        try:
            with open(file_path) as file:
                for line in file.readlines():
                    requirement = line.strip()
                    if (
                        requirement
                        and requirement != "-e ."
                        and not requirement.startswith("-")
                    ):
                        requirements.append(requirement)
        except FileNotFoundError:
            print(f"Requirements file not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading the requirements file: {e}")
    return requirements


setup(
    name="NetworkSecurityMLOps",
    version="0.1.0",
    description="A project for MLOps in network security",
    author="SN Bilgin",
    author_email="senanrbilgin@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=get_requirements("requirements.txt"),
)
