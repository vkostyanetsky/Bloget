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


def write_notes(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given note pages.
    """

    logging.info("Notes building")

    notes = page_writing_utils.get_notes(pages.notes)

    for index, note in enumerate(notes):
        next_note = None if index == 0 else notes[index - 1]
        previous_note = None if index == len(notes) - 1 else notes[index + 1]

        _write_note(note, previous_note, next_note, metadata)


def _write_note(
    note: page_reader.BlogPage,
    previous_note: page_reader.BlogPage | None,
    next_note: page_reader.BlogPage | None,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a given text page.
    """

    logging.info('Building a note from "%s"', note.folder_path)

    folder_path = __get_output_folder_path(note, metadata)

    file_text = __get_file_text(note, previous_note, next_note, metadata)
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)

    page_writing_utils.copy_page_attachments(note, folder_path)


def __get_file_text(
    note: page_reader.BlogPage,
    previous_note: page_reader.BlogPage | None,
    next_note: page_reader.BlogPage | None,
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = __get_template_parameters(
        note, previous_note, next_note, metadata
    )

    return metadata.templates.get_template("note.html").render(template_parameters)


def __get_template_parameters(
    note: page_reader.BlogPage,
    previous_note: page_reader.BlogPage | None,
    next_note: page_reader.BlogPage | None,
    metadata: metadata_reader.BlogMetadata,
) -> dict[str, typing.Any]:
    result = page_writing_utils.get_html_template_parameters(
        metadata=metadata,
        page_title=note.title,
        page_description=note.description,
        page_path=note.path,
        page_is_editable=True,
    )

    if previous_note:
        result["previous_note_path"] = __get_note_page_path(previous_note)
        result["previous_note_title"] = previous_note.title
        result["hotkey_ctrl_left_url"] = __get_note_page_url(
            result["previous_note_path"], metadata
        )
    else:
        result["previous_note_path"] = ""
        result["previous_note_title"] = ""

    if next_note:
        result["next_note_path"] = __get_note_page_path(next_note)
        result["next_note_title"] = next_note.title
        result["hotkey_ctrl_right_url"] = __get_note_page_url(
            result["next_note_path"], metadata
        )
    else:
        result["next_note_path"] = ""
        result["next_note_title"] = ""

    result["note"] = note

    result["tags"] = metadata.tags

    return result


def __get_note_page_url(
    note_page_path: str, metadata: metadata_reader.BlogMetadata
) -> str:
    return f"{metadata.settings['url']}/{note_page_path}"


def __get_output_folder_path(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns path to note's folder.
    """

    result = os.path.join(metadata.paths["output"], constants.NOTES_FOLDER_NAME)

    return os.path.join(result, page.folder_name)


def __get_note_page_path(note: page_reader.BlogPage) -> str:
    """
    Returns a path to a note.

    For instance,
        notes/note_name
        notes/tags/alice/note_name
    """

    path_parts = [constants.NOTES_FOLDER_NAME]

    path_parts.append(note.folder_name)

    return "/".join(path_parts)
