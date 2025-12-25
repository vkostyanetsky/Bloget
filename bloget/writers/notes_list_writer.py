#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

import logging
import os
import typing

from bloget import constants, utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def write_note_lists(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds note list pages.
    """

    logging.info("Note lists building")

    notes = page_writing_utils.get_notes(pages.notes)
    notes_left = len(notes)

    list_number = 1
    list_notes = []
    list_size = 20

    page_count = (len(notes) + list_size - 1) // list_size

    for note in notes:
        list_notes.append(note)
        notes_left -= 1

        if len(list_notes) == list_size or notes_left == 0:
            list_is_last = notes_left == 0

            __write_notes_list(
                list_notes=list_notes,
                list_number=list_number,
                list_is_last=list_is_last,
                page_count=page_count,
                metadata=metadata,
            )

            list_number += 1
            list_notes = []


def __get_note_list_folder_path(
    list_number: int, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns a path to note list folder.

    For instance: D:/Blog/notes/page-1
    """

    result = os.path.join(metadata.paths["output"], constants.NOTES_FOLDER_NAME)

    if list_number > 1:
        result = os.path.join(result, f"page-{list_number}")

    return result


def __write_notes_list(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    list_is_last: bool,
    page_count: int,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Writes a note list.

    Examples:
        notes/index.html
        notes/page-1/index.html
    """

    folder_path = __get_note_list_folder_path(list_number, metadata)

    file_text = __get_notes_list_file_text(
        list_notes, list_number, list_is_last, page_count, metadata
    )
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)


def __get_notes_list_file_text(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    list_is_last: bool,
    page_count: int,
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns template parameters for the note.jinja file.
    """

    template_parameters = __get_note_list_template_parameters(
        list_notes, list_number, list_is_last, page_count, metadata
    )

    return metadata.templates.get_template("notes_list.jinja").render(
        template_parameters
    )


def __get_note_list_page_path(list_number: int) -> str:
    """
    Returns a path of a note list.

    For instance,
        notes
        notes/page-1
    """

    path_parts = [constants.NOTES_FOLDER_NAME]

    if list_number > 1:
        path_parts.append(f"page-{list_number}")

    return "/".join(path_parts)


def __get_note_list_page_url(
    list_number: int, metadata: metadata_reader.BlogMetadata
) -> str:
    url_parts = metadata.settings["url"]
    page_path = __get_note_list_page_path(list_number)

    return f"{url_parts}/{page_path}"


def __get_note_list_template_parameters(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    list_is_last: bool,
    page_count: int,
    metadata: metadata_reader.BlogMetadata,
) -> dict[str, typing.Any]:
    page_title = metadata.language["notes"]
    page_path = __get_note_list_page_path(list_number)

    result = page_writing_utils.get_html_template_parameters_for_service_page(
        metadata=metadata,
        page_title=page_title,
        page_path=page_path,
    )

    result["page"] = list_number
    result["page_notes"] = len(list_notes)
    result["page_count"] = page_count
    result["notes"] = list_notes
    result["tags"] = metadata.tags
    result["notes_folder"] = constants.NOTES_FOLDER_NAME

    if list_number > 1:
        next_list_url = __get_note_list_page_url(list_number - 1, metadata)

        result["next_list_url"] = next_list_url
        result["hotkey_ctrl_right_url"] = next_list_url

    if not list_is_last:
        previous_list_url = __get_note_list_page_url(list_number + 1, metadata)

        result["previous_list_url"] = previous_list_url
        result["hotkey_ctrl_left_url"] = previous_list_url

    return result
