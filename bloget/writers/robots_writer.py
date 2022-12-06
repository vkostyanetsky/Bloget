"""
Implementation of robots.txt building functionality.
"""

import logging
import os

from bloget import utils
from bloget.readers import metadata_reader


def write_robots(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Builds & writes the robots.txt file.
    """

    logging.info("Robots building")

    file_text = __get_file_text(metadata)
    file_path = os.path.join(metadata.paths["output"], "robots.txt")

    utils.make_file(file_path, file_text)


def __get_file_text(metadata: metadata_reader.BlogMetadata) -> str:
    """
    Returns content of the robots.txt file.
    """

    template_parameters = {"settings": metadata.settings}

    return metadata.templates.get_template("robots.txt").render(template_parameters)
