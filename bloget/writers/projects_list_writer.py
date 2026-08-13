#!/usr/bin/env python3

"""
Implementation of projects list page building functionality.
"""

import logging
import os
import typing

from bloget import constants, utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils, taxonomy_utils


def write_projects_list(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds projects list pages: the common one & a list per stack.

    Example: projects/index.html
    """

    logging.info("PROJECT LIST BUILDING...")

    folder_path = os.path.join(metadata.paths["output"], constants.PROJECTS_FOLDER_NAME)

    projects = sorted(pages.projects, key=lambda project: project.created, reverse=True)

    _write_projects_list(
        projects=projects,
        page_path=constants.PROJECTS_FOLDER_NAME,
        folder_path=folder_path,
        stack=None,
        metadata=metadata,
    )

    for project in projects:
        project_folder_path = os.path.join(folder_path, project.folder_name)
        utils.make_folder(project_folder_path)

        page_writing_utils.copy_page_attachments(project, project_folder_path)

    _write_projects_lists_by_stacks(projects, folder_path, metadata)

    logging.info("PROJECT LIST BUILDING DONE")


def _write_projects_lists_by_stacks(
    projects: list[page_reader.BlogPage],
    projects_folder_path: str,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a projects list per stack, so that a stack chip of a project is
    able to lead to a page with projects of the stack only.
    """

    taxonomy_utils.check_folder_names_are_free(
        projects, constants.STACKS_FOLDER_NAME, constants.PROJECTS_FOLDER_NAME
    )

    stacks = taxonomy_utils.get_used_terms(
        projects, metadata.stacks, taxonomy_utils.get_project_stacks
    )

    for stack in stacks:
        logging.info('Builing projects list of the "%s" stack...', stack)

        _write_projects_list(
            projects=projects,
            page_path=taxonomy_utils.get_term_page_path(
                constants.PROJECTS_FOLDER_NAME, constants.STACKS_FOLDER_NAME, stack
            ),
            folder_path=taxonomy_utils.get_term_folder_path(
                projects_folder_path, constants.STACKS_FOLDER_NAME, stack
            ),
            stack=stack,
            metadata=metadata,
        )


def _write_projects_list(
    projects: list[page_reader.BlogPage],
    page_path: str,
    folder_path: str,
    stack: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Writes a projects list.

    Examples:
        projects/index.html
        projects/stacks/react/index.html
    """

    file_path = os.path.join(folder_path, "index.html")
    file_text = _file_text(projects, page_path, stack, metadata)

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)


def _file_text(
    projects: list[page_reader.BlogPage],
    page_path: str,
    stack: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns HTML of the page.
    """

    template_parameters = _get_template_parameters(projects, page_path, stack, metadata)

    return metadata.templates.get_template("projects_list.jinja").render(
        template_parameters
    )


def _get_page_title(stack: str | None, metadata: metadata_reader.BlogMetadata) -> str:
    """
    Returns a title of a projects list: a common one, or a one of a stack.
    """

    result = metadata.language["projects"]

    if stack is not None:
        result = f"{result}: {taxonomy_utils.get_term_title(metadata.stacks, stack)}"

    return result


def _get_template_parameters(
    projects: list[page_reader.BlogPage],
    page_path: str,
    stack: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> dict[str, typing.Any]:

    result = page_writing_utils.get_html_template_parameters_for_service_page(
        metadata=metadata,
        page_title=_get_page_title(stack, metadata),
        page_path=page_path,
    )

    result["projects"] = projects
    result["projects_folder"] = constants.PROJECTS_FOLDER_NAME

    # A pre-generated list of a stack knows the stack it is filtered by, so
    # that its chips are able to show which filter is applied.

    result["active_stack"] = stack if stack is not None else ""

    return result
