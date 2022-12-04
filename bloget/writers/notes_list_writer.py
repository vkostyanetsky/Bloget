#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

import logging
import os

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

    __write_note_lists_by_selected_tag(
        pages=pages, selected_tag=None, metadata=metadata
    )

    for selected_tag in metadata.tags:

        __write_note_lists_by_selected_tag(
            pages=pages, selected_tag=selected_tag, metadata=metadata
        )


def __get_notes_by_tag(
    notes: list[page_reader.BlogPage], tag: str | None
) -> list[page_reader.BlogPage]:
    """
    Filters lists of notes by a tag given.
    """

    notes = list(filter(lambda note: tag is None or tag in note.tags, notes))

    return sorted(notes, key=lambda note: note.created, reverse=True)


def __write_note_lists_by_selected_tag(
    pages: pages_reader.BlogPages,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Writes note list pages by selected tag.
    """

    notes = __get_notes_by_tag(pages.notes, selected_tag)
    notes_left = len(notes)

    list_number = 1
    list_notes = []
    list_size = 20

    for note in notes:

        list_notes.append(note)
        notes_left -= 1

        if len(list_notes) == list_size or notes_left == 0:

            is_last_list = notes_left == 0

            if list_number == 1:
                __write_notes_list(
                    list_notes=list_notes,
                    list_number=0,
                    selected_tag=selected_tag,
                    is_last_list=is_last_list,
                    metadata=metadata,
                )

            __write_notes_list(
                list_notes=list_notes,
                list_number=list_number,
                selected_tag=selected_tag,
                is_last_list=is_last_list,
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

    if list_number > 0:
        result = os.path.join(result, f"page-{list_number}")

    return result


def __write_notes_list(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    selected_tag: str | None,
    is_last_list: bool,
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
        list_notes, list_number, selected_tag, metadata
    )
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)


def __get_notes_list_file_text(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = __get_note_list_template_parameters(
        list_notes, list_number, selected_tag, metadata
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
    Returns a title of a note list.

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

    if list_number > 0:
        path_parts.append(f"page-{list_number}")

    return "/".join(path_parts)


def __get_note_list_template_parameters(
    list_notes: list[page_reader.BlogPage],
    list_number: int,
    selected_tag: str | None,
    metadata: metadata_reader.BlogMetadata,
) -> dict[str, str | list[page_reader.BlogPage]]:

    page_title = __get_note_list_page_title(selected_tag, metadata)
    page_path = __get_note_list_page_path(list_number, selected_tag)

    result = page_writing_utils.get_html_template_parameters(
        metadata=metadata,
        page_title=page_title,
        page_path=page_path,
        page_is_editable=False,
    )

    result["tags"] = metadata.tags
    result["notes"] = list_notes

    return result


# def get_notes_page_url(page_number: int):
#
#     result = config['url'] + '/notes/'
#
#     if selected_tag is not None:
#         result = result + 'tags/' + selected_tag + '/'
#
#     if page_number > 1:
#         result = result + 'page-' + str(page_number) + '/'
#
#     return result

# def build_note_lists():
#
#     def build_page(page_number):
#
#
#
#     if selected_tag is None:
#
#         notes = pages['notes']
#
#         page_parent_dirpath = paths['project_notes_dirpath']
#         page_parent_path = '/notes/'
#
#     else:
#
#         notes = get_notes_by_tag(pages['notes'], selected_tag)
#
#         page_parent_dirpath = os.path.join(paths['project_notes_dirpath'], 'tags', selected_tag)
#         page_parent_path = '/notes/tags/' + selected_tag + '/'
#
