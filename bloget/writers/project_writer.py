"""
Implementation of project pages building functionality.
"""

import logging
import os

from bloget import utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def write_projects(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given project pages.
    """

    logging.info("Projects building")

    for project in pages.projects:
        _write_project(project, metadata)


def _write_project(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a given project page.
    """

    logging.info('Building a project from "%s"', page.folder_path)

    output_folder_path = os.path.join(metadata.paths["output"], page.path)

    logging.debug('Page path: "%s"', page.path)
    logging.debug('Output folder path: "%s"', output_folder_path)

    file_text = __get_file_text(page, metadata)
    file_path = os.path.join(output_folder_path, "index.html")

    utils.make_folder(output_folder_path)
    utils.make_file(file_path, file_text)

    page_writing_utils.copy_page_attachments(page, output_folder_path)


def __get_file_text(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns template parameters for the text.jinja file.
    """

    template_parameters = page_writing_utils.get_html_template_parameters(
        metadata=metadata,
        page_title=page.title,
        page_description=page.description,
        page_path=page.path,
        page_is_editable=True,
    )

    template_parameters["tags"] = page.tags
    template_parameters["page_text"] = page.text

    return metadata.templates.get_template("project.jinja").render(template_parameters)
