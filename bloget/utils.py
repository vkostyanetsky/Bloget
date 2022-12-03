#!/usr/bin/env python3

"""
Implementation of methods intended to be used by various files.
"""

import logging
import os
import sys

import yaml

from bloget import constants
from bloget.readers import metadata_reader


def raise_error(message: str) -> None:
    """
    Writes an error message to a log, then shuts down the application.
    """

    logging.critical(message)
    sys.exit("A critical error has occurred. Exiting...")


def make_file(path: str, data: str) -> None:
    """
    Makes a file.
    """

    logging.debug(f'Making a file "{path}"...')

    try:

        with open(path, "w+", encoding=constants.ENCODING) as file:
            file.write(data)

    except IOError:

        raise_error(f"Unable to make a file: {path}")


def make_folder(path: str) -> None:
    """
    Makes a directory is it doesn't exist.
    """

    logging.debug(f'Making a folder "{path}"...')

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


def get_html_template_parameters(
    metadata: metadata_reader.BlogMetadata,
    page_title: str,
    page_path: str,
    page_is_editable: bool,
) -> dict[str, str | dict[str, str]]:
    """
    Returns common parameters for HTML templates.
    """

    page_edit_url = __get_page_edit_url(metadata, page_path, page_is_editable)

    return {
        "language": metadata.language,
        "settings": metadata.settings,
        "page_title": page_title,
        "page_path": page_path,
        "page_edit_url": page_edit_url,
    }


def __get_page_edit_url(
    metadata: metadata_reader.BlogMetadata, page_path: str, page_is_editable: bool
) -> str:
    """
    Determines if a page can be edited, then makes a link to GitHub.
    """

    result = ""

    if page_is_editable and metadata.settings.get("github_repository"):

        parts = [
            f"https://github.com/{metadata.settings['github_repository']}/edit/main"
        ]

        if page_path:
            parts.append(page_path)

        parts.append("index.md")

        result = "/".join(parts)

    return result
