#!/usr/bin/env python3

"""
Implementation of methods intended to be used by various files.
"""

import logging
import os
import shutil
import sys

import yaml

from bloget import constants


def raise_error(message: str) -> None:
    """
    Writes an error message to a log, then shuts down the application.
    """

    logging.critical(message)
    sys.exit("A critical error has occurred. Exiting...")


def copy_file(source_path: str, target_path: str) -> None:
    """
    Copies file or folder.
    """

    logging.debug('Copying "%s" to "%s"...', source_path, target_path)

    try:
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)

    except IOError:
        raise_error(f'Unable to copy "{source_path}" to: {target_path}')


def make_file(path: str, data: str) -> None:
    """
    Makes a file.
    """

    logging.debug('Making a file "%s"...', path)

    try:
        with open(path, "w+", encoding=constants.ENCODING) as file:
            file.write(data)

    except IOError:
        raise_error(f"Unable to make a file: {path}")


def make_folder(path: str) -> None:
    """
    Makes a directory is it doesn't exist.
    """

    logging.debug('Making a folder "%s"...', path)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except IOError:
            raise_error(f"Unable to make a folder: {path}")


def read_yaml_file(file_path: str) -> dict[str, str]:
    """
    Returns content of YAML files as a dictionary.
    """

    result: dict[str, str] = {}

    try:
        with open(file=file_path, encoding=constants.ENCODING) as yaml_file:
            result = yaml.safe_load(yaml_file)

    except IOError:
        raise_error(f"Unable to read a file: {file_path}")

    return result
