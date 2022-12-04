#!/usr/bin/env python3

"""
Common methods which are applicable to both types of pages (texts & notes).
"""

import logging
import os
import shutil

from bloget import utils
from bloget.readers import metadata_reader, page_reader


def copy_page_attachments(page: page_reader.BlogPage, output_folder_path: str) -> None:
    """
    Copies page's attachments to the page build folder.
    """

    if page.attachments:

        logging.info("Copying attachments...")

        for attachment in page.attachments:

            source_file_path = os.path.join(page.folder_path, attachment)
            target_file_path = os.path.join(output_folder_path, attachment)

            logging.debug('Copying attachment from "%s"...', attachment)

            try:
                shutil.copyfile(source_file_path, target_file_path)
            except IOError:
                utils.raise_error(f"Unable to copy file: {source_file_path}")

        logging.info("Copying attachments has been done!")


def get_html_template_parameters(
    metadata: metadata_reader.BlogMetadata,
    page_title: str,
    page_path: str,
    page_is_editable: bool,
) -> dict[str, str | dict[str, str]]:
    """
    Returns common parameters for HTML templates.
    """

    page_edit_url = __get_page_edit_url(metadata, page_path, page_is_editable)

    return {
        "language": metadata.language,
        "settings": metadata.settings,
        "page_title": page_title,
        "page_path": page_path,
        "page_edit_url": page_edit_url,
    }


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
