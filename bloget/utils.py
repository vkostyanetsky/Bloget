#!/usr/bin/env python3

"""
Implementation of methods intended to be used by various files.
"""

import logging
import os
import sys

import yaml

from bloget import constants


def raise_error(message: str) -> None:
    """
    Writes an error message to a log, then shuts down the application.
    """

    logging.critical(message)
    sys.exit("A critical error has occurred. Exiting...")


def make_folder(path: str) -> None:
    """
    Makes a directory is it doesn't exist.
    """

    logging.info(f'Making a folder "{path}"...')

    if not os.path.exists(path):

        try:
            os.makedirs(path)
        except IOError:
            raise_error(f"Unable to make a folder: {path}")


def read_yaml_file(file_path: str) -> dict:
    """
    Returns content of YAML files as a dictionary.
    """

    try:
        with open(file=file_path, encoding=constants.ENCODING) as yaml_file:
            result = yaml.safe_load(yaml_file)

    except IOError:
        raise_error(f"Unable to read a file: {file_path}")

    return result