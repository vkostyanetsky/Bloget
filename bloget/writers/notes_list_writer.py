#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

import logging
import os
import typing
from dataclasses import dataclass

from bloget import constants, utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils, taxonomy_utils

LIST_SIZE = 20


@dataclass
class NoteLists:
    """
    A container with notes to split into lists, and with a place to write the
    lists in: the common one, or a one of a tag.
    """

    notes: list[page_reader.BlogPage]
    path: str
    folder_path: str
    tag: str | None

    @property
    def page_count(self) -> int:
        """
        Returns a number of lists the notes are split into.

        Even when there are no notes at all, the first (empty) list has to be
        written: otherwise the blog gets no notes/index.html page.
        """

        return max(1, (len(self.notes) + LIST_SIZE - 1) // LIST_SIZE)

    def get_list_notes(self, list_number: int) -> list[page_reader.BlogPage]:
        """
        Returns notes of a list by its number.
        """

        first_note = (list_number - 1) * LIST_SIZE

        return self.notes[first_note : first_note + LIST_SIZE]


def write_note_lists(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds note list pages: the common ones & a set of lists per tag.
    """

    logging.info("NOTE LISTS BUILIDNG...")

    notes = page_writing_utils.get_notes(pages.notes)
    notes_folder_path = os.path.join(
        metadata.paths["output"], constants.NOTES_FOLDER_NAME
    )

    _write_note_lists(
        NoteLists(
            notes=notes,
            path=constants.NOTES_FOLDER_NAME,
            folder_path=notes_folder_path,
            tag=None,
        ),
        metadata,
    )

    _write_note_lists_by_tags(notes, notes_folder_path, metadata)

    logging.info("NOTE LISTS BUILIDNG DONE")


def _write_note_lists_by_tags(
    notes: list[page_reader.BlogPage],
    notes_folder_path: str,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds note lists per tag, so that a tag chip of a note is able to lead to
    a page with notes of the tag only.
    """

    taxonomy_utils.check_folder_names_are_free(
        notes, constants.TAGS_FOLDER_NAME, constants.NOTES_FOLDER_NAME
    )

    tags = taxonomy_utils.get_used_terms(
        notes, metadata.tags, taxonomy_utils.get_note_tags
    )

    for tag in tags:
        logging.info('Builing note lists of the "%s" tag...', tag)

        _write_note_lists(
            NoteLists(
                notes=taxonomy_utils.get_pages_by_term(
                    notes, tag, taxonomy_utils.get_note_tags
                ),
                path=taxonomy_utils.get_term_page_path(
                    constants.NOTES_FOLDER_NAME, constants.TAGS_FOLDER_NAME, tag
                ),
                folder_path=taxonomy_utils.get_term_folder_path(
                    notes_folder_path, constants.TAGS_FOLDER_NAME, tag
                ),
                tag=tag,
            ),
            metadata,
        )


def _write_note_lists(lists: NoteLists, metadata: metadata_reader.BlogMetadata) -> None:
    """
    Writes every list of the notes given.
    """

    for list_number in range(1, lists.page_count + 1):
        _write_notes_list(lists, list_number, metadata)


def _get_note_list_folder_path(lists: NoteLists, list_number: int) -> str:
    """
    Returns a path to note list folder.

    For instance: D:/Blog/notes/page-1
    """

    return (
        lists.folder_path
        if list_number == 1
        else os.path.join(lists.folder_path, f"page-{list_number}")
    )


def _write_notes_list(
    lists: NoteLists, list_number: int, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Writes a note list.

    Examples:
        notes/index.html
        notes/page-1/index.html
        notes/tags/python/index.html
    """

    folder_path = _get_note_list_folder_path(lists, list_number)

    logging.info("Builing note list #%d...", list_number)

    file_text = _get_notes_list_file_text(lists, list_number, metadata)
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)


def _get_notes_list_file_text(
    lists: NoteLists, list_number: int, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns template parameters for the note.jinja file.
    """

    template_parameters = _get_note_list_template_parameters(
        lists, list_number, metadata
    )

    return metadata.templates.get_template("notes_list.jinja").render(
        template_parameters
    )


def _get_note_list_page_path(lists: NoteLists, list_number: int) -> str:
    """
    Returns a path of a note list.

    For instance,
        notes
        notes/page-1
        notes/tags/python
    """

    return lists.path if list_number == 1 else f"{lists.path}/page-{list_number}"


def _get_note_list_page_url(
    lists: NoteLists, list_number: int, metadata: metadata_reader.BlogMetadata
) -> str:
    url_parts = metadata.settings["url"]
    page_path = _get_note_list_page_path(lists, list_number)

    return f"{url_parts}/{page_path}"


def _get_note_list_page_title(
    lists: NoteLists, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns a title of a note list: a common one, or a one of a tag.
    """

    result = metadata.language["notes"]

    if lists.tag is not None:
        result = f"{result}: {taxonomy_utils.get_term_title(metadata.tags, lists.tag)}"

    return result


def _get_note_list_template_parameters(
    lists: NoteLists, list_number: int, metadata: metadata_reader.BlogMetadata
) -> dict[str, typing.Any]:
    list_notes = lists.get_list_notes(list_number)

    page_title = _get_note_list_page_title(lists, metadata)
    page_path = _get_note_list_page_path(lists, list_number)

    result = page_writing_utils.get_html_template_parameters_for_service_page(
        metadata=metadata,
        page_title=page_title,
        page_path=page_path,
    )

    result["page"] = list_number
    result["page_notes"] = len(list_notes)
    result["page_count"] = lists.page_count
    result["notes"] = list_notes
    result["tags"] = metadata.tags
    result["notes_folder"] = constants.NOTES_FOLDER_NAME

    # A pre-generated list of a tag knows the tag it is filtered by, so that
    # its chips are able to show which filter is applied.

    result["active_tag"] = lists.tag if lists.tag is not None else ""

    if list_number > 1:
        next_list_url = _get_note_list_page_url(lists, list_number - 1, metadata)

        result["next_list_url"] = next_list_url
        result["hotkey_ctrl_right_url"] = next_list_url

    if list_number < lists.page_count:
        previous_list_url = _get_note_list_page_url(lists, list_number + 1, metadata)

        result["previous_list_url"] = previous_list_url
        result["hotkey_ctrl_left_url"] = previous_list_url

    return result
