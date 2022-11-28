from setuptools import find_packages, setup

from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    """
    Description: This function returns packages from requirements file as a list.
    =========================================================
    return List containing packages to be installed.
    """
    # A file named "requirements.txt", will be opened with the reading mode.
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()

    # Remove new line character from the end of the line
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    # Removing "-e ." from the end of the list as it is not a package name and only used to trigger "setup.py".
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list


setup(
    name="sensor",
    version="0.0.1",
    author="SatyaNerurkar",
    author_email="satyanerurkar@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements(),
)