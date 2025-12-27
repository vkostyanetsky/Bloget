#!/usr/bin/env python3

"""
Implementation of projects list page building functionality.
"""

import logging
import os
import typing

from bloget import constants, utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def write_projects_list(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds projects list page.

    Example: projects/index.html
    """

    logging.info("Projects list page building")

    folder_path = os.path.join(metadata.paths["output"], constants.PROJECTS_FOLDER_NAME)

    file_path = os.path.join(folder_path, "index.html")
    file_text = _file_text(pages.projects, metadata)

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)

    projects = sorted(pages.projects, key=lambda project: project.created, reverse=True)

    for project in projects:

        project_folder_path = os.path.join(folder_path, project.folder_name)
        utils.make_folder(project_folder_path)

        page_writing_utils.copy_page_attachments(project, project_folder_path)


def _file_text(
    projects: list[page_reader.BlogPage], metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns HTML of the page.
    """

    template_parameters = _get_template_parameters(projects, metadata)

    return metadata.templates.get_template("projects_list.jinja").render(
        template_parameters
    )


def _get_template_parameters(
    projects: list[page_reader.BlogPage], metadata: metadata_reader.BlogMetadata
) -> dict[str, typing.Any]:

    result = page_writing_utils.get_html_template_parameters_for_service_page(
        metadata=metadata,
        page_title=metadata.language["projects"],
        page_path=constants.PROJECTS_FOLDER_NAME,
    )

    result["projects"] = projects

    return result
