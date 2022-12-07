#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

import logging
import os

from bloget import constants, utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def write_notes(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given note pages.
    """

    __write_notes_by_selected_tag(pages=pages, selected_tag=None, metadata=metadata)

    for selected_tag in metadata.tags:
        __write_notes_by_selected_tag(
            pages=pages, selected_tag=selected_tag, metadata=metadata
        )


def __write_notes_by_selected_tag(
    pages: pages_reader.BlogPages,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> None:

    tag_comment = page_writing_utils.get_selected_tag_comment(selected_tag)
    logging.info("Notes building %s", tag_comment)

    for page in pages.notes:

        if selected_tag is None or selected_tag in page.tags:
            __write_note(page, metadata, selected_tag)


def __write_note(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
    selected_tag: str | None,
) -> None:
    """
    Builds a given text page.
    """

    logging.info('Building a note from "%s"', page.folder_path)

    folder_path = __get_output_folder_path(page, metadata, selected_tag)

    file_text = __get_file_text(page, metadata, selected_tag)
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)

    # No need to copy attachments to note slices for notes/tags/*/<note_name>;
    # it must be done for notes/<note_name> only.

    if selected_tag is None:
        page_writing_utils.copy_page_attachments(page, folder_path)


def __get_file_text(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
    selected_tag: str | None,
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = __get_template_parameters(page, metadata, selected_tag)
    template_parameters["page_text"] = page.text

    return metadata.templates.get_template("text.html").render(template_parameters)


def __get_template_parameters(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
    selected_tag: str | None,
) -> dict[str, str | list[page_reader.BlogPage] | dict[str, str] | None]:

    result = page_writing_utils.get_html_template_parameters(
        metadata=metadata,
        page_title=page.title,
        page_path=page.path,
        page_is_editable=True,
    )

    result["tags"] = metadata.tags
    result["selected_tag"] = selected_tag

    return result


def __get_output_folder_path(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
    selected_tag: str | None,
) -> str:
    """
    Returns path to note's folder.
    """

    result = os.path.join(metadata.paths["output"], constants.NOTES_FOLDER_NAME)

    if selected_tag is not None:
        result = os.path.join(result, "tags", selected_tag)

    return os.path.join(result, page.folder_name)
