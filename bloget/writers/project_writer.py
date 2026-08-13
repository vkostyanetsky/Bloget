"""
Implementation of project pages building functionality.
"""

import logging

from bloget import constants
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils, taxonomy_utils


def write_projects(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given project pages.
    """

    logging.info("PROJECTS BUILDING...")

    stack_urls = _get_stack_urls(pages.projects, metadata)

    for project in pages.projects:
        _write_project(project, stack_urls, metadata)

    logging.info("PROJECTS BUILDING DONE")


def _get_stack_urls(
    projects: list[page_reader.BlogPage], metadata: metadata_reader.BlogMetadata
) -> dict[str, str]:
    """
    Returns URLs of pre-generated projects lists by their stacks.

    Every stack a project has is here, since projects_list_writer writes a
    list for each of them.
    """

    stacks = taxonomy_utils.get_used_terms(
        projects, metadata.stacks, taxonomy_utils.get_project_stacks
    )

    return taxonomy_utils.get_term_page_urls(
        metadata, constants.PROJECTS_FOLDER_NAME, constants.STACKS_FOLDER_NAME, stacks
    )


def _write_project(
    page: page_reader.BlogPage,
    stack_urls: dict[str, str],
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a given project page.
    """

    logging.info('Building project from "%s"', page.folder_path)

    file_content = _get_project_file_content(page, stack_urls, metadata)
    page_writing_utils.make_index_file(file_content, page, metadata)


def _get_project_file_content(
    page: page_reader.BlogPage,
    stack_urls: dict[str, str],
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns template for the text.jinja file.
    """

    template_parameters = page_writing_utils.html_template_parameters_for_page(
        page, metadata
    )
    template_parameters["page_stacks"] = page.metadata.stacks
    template_parameters["stack_urls"] = stack_urls

    return metadata.templates.get_template("project.jinja").render(template_parameters)
