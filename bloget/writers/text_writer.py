"""
Implementation of text pages building functionality.
"""

import logging

from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def write_texts(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given text pages.
    """

    logging.info("Texts building")

    for text in pages.texts:
        _write_text(text, metadata)


def _write_text(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a given text page.
    """

    logging.info('Building a text from "%s"', page.folder_path)

    file_content = _get_text_file_content(page, metadata)
    page_writing_utils.make_index_file(file_content, page, metadata)


def _get_text_file_content(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns template parameters for the text.jinja file.
    """

    template_parameters = page_writing_utils.html_template_parameters_for_page(
        page, metadata
    )
    template_parameters["tags"] = page.tags

    return metadata.templates.get_template("text.jinja").render(template_parameters)
