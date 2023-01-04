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

    notes = page_writing_utils.get_notes_by_tag(pages.notes, selected_tag)

    for index, note in enumerate(notes):

        previous_note = None if index == 0 else notes[index - 1]
        next_note = None if len(notes) - 1 == index else notes[index + 1]

        __write_note(note, previous_note, next_note, selected_tag, metadata)


def __write_note(
    note: page_reader.BlogPage,
    previous_note: page_reader.BlogPage | None,
    next_note: page_reader.BlogPage | None,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds a given text page.
    """

    logging.info('Building a note from "%s"', note.folder_path)

    folder_path = __get_output_folder_path(note, metadata, selected_tag)

    file_text = __get_file_text(note, previous_note, next_note, selected_tag, metadata)
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)

    # No need to copy attachments to note slices for notes/tags/*/<note_name>;
    # it must be done for notes/<note_name> only.

    if selected_tag is None:
        page_writing_utils.copy_page_attachments(note, folder_path)


def __get_file_text(
    note: page_reader.BlogPage,
    previous_note: page_reader.BlogPage | None,
    next_note: page_reader.BlogPage | None,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = __get_template_parameters(
        note, previous_note, next_note, selected_tag, metadata
    )

    return metadata.templates.get_template("note.html").render(template_parameters)


def __get_template_parameters(
    note: page_reader.BlogPage,
    previous_note: page_reader.BlogPage | None,
    next_note: page_reader.BlogPage | None,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> dict[str, typing.Any]:

    result = page_writing_utils.get_html_template_parameters(
        metadata=metadata,
        page_title=note.title,
        page_description=note.description,
        page_path=note.path,
        page_is_editable=True,
    )

    result["previous_note_path"] = (
        __get_note_page_path(previous_note, selected_tag) if previous_note else ""
    )
    result["previous_note_title"] = previous_note.title if previous_note else ""

    result["next_note_path"] = (
        __get_note_page_path(next_note, selected_tag) if next_note else ""
    )
    result["next_note_title"] = next_note.title if next_note else ""

    result["note"] = note

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


def __get_note_page_path(note: page_reader.BlogPage, selected_tag: str | None) -> str:
    """
    Returns a path to a note.

    For instance,
        notes/note_name
        notes/tags/alice/note_name
    """

    path_parts = [constants.NOTES_FOLDER_NAME]

    if selected_tag is not None:
        path_parts.append("tags")
        path_parts.append(selected_tag)

    path_parts.append(note.folder_name)

    return "/".join(path_parts)
