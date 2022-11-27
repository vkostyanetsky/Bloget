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


def make_directory(path: str) -> None:
    """
    Makes a directory is it doesn't exist.
    """

    if not os.path.exists(path):
        os.mkdir(path)


def read_yaml_file(file_path: str) -> dict:
    """
    Returns content of YAML files as a dictionary.
    """

    try:
        with open(file=file_path, encoding=constants.ENCODING) as yaml_file:
            result = yaml.safe_load(yaml_file)

    except IOError:
        raise_error(f"Unable to read a file by path: {file_path}")

    return result
