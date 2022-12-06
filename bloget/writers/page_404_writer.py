"""
Implementation of page 404 building functionality.
"""

import logging
import os

from bloget import utils
from bloget.readers import metadata_reader
from bloget.writers.utils import page_writing_utils


def write_page_404(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Builds & writes the 404 page.
    """

    logging.info("Building page 404")

    file_text = __get_file_text(metadata)
    file_path = os.path.join(metadata.paths["output"], "404.html")

    utils.make_file(file_path, file_text)


def __get_file_text(metadata: metadata_reader.BlogMetadata) -> str:
    """
    Returns content of the page 404 file.
    """

    template_parameters = page_writing_utils.get_html_template_parameters(
        metadata=metadata,
        page_title=metadata.language["page_404_title"],
        page_path="404.html",
        page_is_editable=False,
    )

    return metadata.templates.get_template("404.html").render(template_parameters)
