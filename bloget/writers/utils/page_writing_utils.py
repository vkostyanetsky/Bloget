#!/usr/bin/env python3

"""
Common methods which are applicable to both types of pages (texts & notes).
"""

import logging
import os
import typing

from bloget import utils
from bloget.readers import metadata_reader, page_reader


def get_notes(notes: list[page_reader.BlogPage]) -> list[page_reader.BlogPage]:
    """
    Filters notes list, then sorts it.
    """

    return sorted(notes, key=lambda note: note.created, reverse=True)


def copy_page_attachments(page: page_reader.BlogPage, output_folder_path: str) -> None:
    """
    Copies page's attachments to the page build folder.
    """

    if page.attachments:
        for attachment in page.attachments:
            logging.debug('Copying attachment from "%s"', attachment)

            source_file_path = os.path.join(page.folder_path, attachment)
            target_file_path = os.path.join(output_folder_path, attachment)

            utils.copy_file(source_file_path, target_file_path)


def get_html_template_parameters(
    metadata: metadata_reader.BlogMetadata,
    page_title: str,
    page_description: str,
    page_path: str,
    page_is_editable: bool,
) -> dict[str, typing.Any]:
    """
    Returns common parameters for HTML templates.
    """

    page_edit_url = __get_page_edit_url(metadata, page_path, page_is_editable)

    return {
        "language": metadata.language,
        "settings": metadata.settings,
        "page_title": page_title,
        "page_description": page_description,
        "page_path": page_path,
        "page_edit_url": page_edit_url,
    }


def get_html_template_parameters_for_service_page(
    metadata: metadata_reader.BlogMetadata,
    page_title: str,
    page_path: str,
) -> dict[str, typing.Any]:
    """
    Returns common parameters for HTML templates.
    """

    return get_html_template_parameters(
        metadata=metadata,
        page_title=page_title,
        page_description="",
        page_path=page_path,
        page_is_editable=False,
    )


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
