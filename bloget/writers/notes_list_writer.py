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

    __write_note_lists_by_selected_tag(
        pages=pages, selected_tag=None, metadata=metadata
    )

    for selected_tag in metadata.tags:
        __write_note_lists_by_selected_tag(
            pages=pages, selected_tag=selected_tag, metadata=metadata
        )


def __write_note_lists_by_selected_tag(
    pages: pages_reader.BlogPages,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Writes note list pages by selected tag.
    """

    tag_comment = page_writing_utils.get_selected_tag_comment(selected_tag)
    logging.info("Note lists building %s", tag_comment)

    notes = page_writing_utils.get_notes_by_tag(pages.notes, selected_tag)
    notes_left = len(notes)

    list_number = 1
    list_notes = []
    list_size = 20

    for note in notes:
        list_notes.append(note)
        notes_left -= 1

        if len(list_notes) == list_size or notes_left == 0:
            list_is_last = notes_left == 0

            __write_notes_list(
                list_notes=list_notes,
                list_number=list_number,
                list_is_last=list_is_last,
                selected_tag=selected_tag,
                metadata=metadata,
            )

            list_number += 1
            list_notes = []


def __get_note_list_folder_path(
    list_number: int, selected_tag: str | None, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns a path to note list folder.

    For instance: D:/Blog/notes/tags/alice/page-1
    """

    result = os.path.join(metadata.paths["output"], constants.NOTES_FOLDER_NAME)

    if selected_tag is not None:
        result = os.path.join(result, "tags", selected_tag)

    if list_number > 1:
        result = os.path.join(result, f"page-{list_number}")

    return result


def __write_notes_list(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    list_is_last: bool,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Writes a note list.

    Without a selected tag:
        notes/index.html
        notes/page-1/index.html

    With a selected tag "alice":
        notes/tags/alice/index.html
        notes/tags/alice/page-1/index.html
    """

    folder_path = __get_note_list_folder_path(list_number, selected_tag, metadata)

    file_text = __get_notes_list_file_text(
        list_notes, list_number, list_is_last, selected_tag, metadata
    )
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)


def __get_notes_list_file_text(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    list_is_last: bool,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = __get_note_list_template_parameters(
        list_notes, list_number, list_is_last, selected_tag, metadata
    )

    return metadata.templates.get_template("notes_list.html").render(
        template_parameters
    )


def __get_note_list_page_title(
    selected_tag: str | None, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns a title of a note list.

    For instance,
        Notes (no tag selected)
        Alice ("alice" tag selected whose title is "alice")
    """

    if selected_tag is None:
        result = metadata.language["notes"]
    else:
        result = (
            metadata.tags[selected_tag][:1].upper() + metadata.tags[selected_tag][1:]
        )

    return result


def __get_note_list_page_path(list_number: int, selected_tag: str | None) -> str:
    """
    Returns a path of a note list.

    For instance,
        notes
        notes/page-1
        notes/tags/alice/
        notes/tags/alice/page-1
    """

    path_parts = [constants.NOTES_FOLDER_NAME]

    if selected_tag is not None:
        path_parts.append("tags")
        path_parts.append(selected_tag)

    if list_number > 1:
        path_parts.append(f"page-{list_number}")

    return "/".join(path_parts)


def __get_note_list_page_url(
    list_number: int, selected_tag: str | None, metadata: metadata_reader.BlogMetadata
) -> str:
    url_parts = metadata.settings["url"]
    page_path = __get_note_list_page_path(list_number, selected_tag)

    return f"{url_parts}/{page_path}"


def __get_note_list_template_parameters(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    list_is_last: bool,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> dict[str, typing.Any]:
    page_title = __get_note_list_page_title(selected_tag, metadata)
    page_path = __get_note_list_page_path(0, selected_tag)

    result = page_writing_utils.get_html_template_parameters_for_service_page(
        metadata=metadata,
        page_title=page_title,
        page_path=page_path,
    )

    result["selected_tag"] = selected_tag
    result["tags"] = metadata.tags
    result["notes"] = list_notes

    if list_number > 1:
        next_list_url = __get_note_list_page_url(
            list_number - 1, selected_tag, metadata
        )

        result["next_list_url"] = next_list_url
        result["hotkey_ctrl_up_url"] = next_list_url

    if not list_is_last:
        previous_list_url = __get_note_list_page_url(
            list_number + 1, selected_tag, metadata
        )

        result["previous_list_url"] = previous_list_url
        result["hotkey_ctrl_down_url"] = previous_list_url

    return result
