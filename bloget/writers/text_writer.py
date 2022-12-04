"""
Implementation of text pages building functionality.
"""
import logging
import os

from bloget import utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers import page_writer


def write_texts(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given text pages.
    """

    logging.info("Texts building")

    for text in pages.texts:
        __write_text(text, metadata)


def __write_text(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a given text page.
    """

    logging.info('Building a text from "%s"', page.folder_path)

    output_folder_path = os.path.join(metadata.paths["output"], page.path)

    logging.debug('Page path: "%s"', page.path)
    logging.debug('Output folder path: "%s"', output_folder_path)

    file_text = __get_file_text(page, metadata)
    file_path = os.path.join(output_folder_path, "index.html")

    utils.make_folder(output_folder_path)
    utils.make_file(file_path, file_text)

    page_writer.copy_page_attachments(page, output_folder_path)


def __get_file_text(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns template parameters for the text.html file.
    """

    template_parameters = page_writer.get_html_template_parameters(
        metadata=metadata,
        page_title=page.title,
        page_path=page.path,
        page_is_editable=True,
    )

    template_parameters["page_text"] = page.text

    return metadata.templates.get_template("text.html").render(template_parameters)
