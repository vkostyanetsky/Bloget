"""
Implementation of project pages building functionality.
"""

import logging

from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def write_projects(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given project pages.
    """

    logging.info("PROJECTS BUILDING...")

    for project in pages.projects:
        _write_project(project, metadata)

    logging.info("PROJECTS BUILDING DONE")


def _write_project(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a given project page.
    """

    logging.info('Building project from "%s"', page.folder_path)

    file_content = _get_project_file_content(page, metadata)
    page_writing_utils.make_index_file(file_content, page, metadata)


def _get_project_file_content(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns template for the text.jinja file.
    """

    template_parameters = page_writing_utils.html_template_parameters_for_page(
        page, metadata
    )
    template_parameters["page_stacks"] = page.metadata.stacks

    return metadata.templates.get_template("project.jinja").render(template_parameters)
