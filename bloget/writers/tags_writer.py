#!/usr/bin/env python3

"""
Implementation of tags page building functionality.
"""

import logging
import os
import typing

from bloget import constants, utils
from bloget.readers import metadata_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def write_tags(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds tags page and writes it at notes/tags/index.html
    """

    logging.info("Tags building")

    tag_counters = __get_tag_counters(pages, metadata)
    folder_path = __get_tags_folder_path(metadata)
    file_text = __get_tags_file_text(tag_counters, metadata)
    file_path = os.path.join(folder_path, "index.html")

    utils.make_folder(folder_path)
    utils.make_file(file_path, file_text)


def __get_tag_counters(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> list[dict]:
    """
    Makes a dictionary with tags and number of occurrences of them in notes:

    For example:
    [
        {
            "name": "egg",
            "counter": 1,
        },
        {
            "name": "chicken",
            "counter": 1,
        },
    ]
    """

    counters = {}

    for tag in metadata.tags:
        counters[tag] = 0

    for note in pages.notes:
        for tag in note.tags:
            counters[tag] += 1

    result = []

    for tag_name in counters:
        tag_counter = counters[tag_name]

        if tag_counter:
            result.append({"name": tag_name, "counter": tag_counter})

    return sorted(result, key=lambda x: x["counter"], reverse=True)


def __get_tags_folder_path(metadata: metadata_reader.BlogMetadata) -> str:
    """
    Returns a path to note list folder.

    For instance: D:/Blog/notes/tags/alice/page-1
    """

    notes_path = os.path.join(metadata.paths["output"], constants.NOTES_FOLDER_NAME)

    return os.path.join(notes_path, "tags")


def __get_tags_file_text(
    tag_counters: list[dict],
    metadata: metadata_reader.BlogMetadata,
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = __get_tags_template_parameters(tag_counters, metadata)

    return metadata.templates.get_template("tags.html").render(template_parameters)


def __get_tags_page_title(metadata: metadata_reader.BlogMetadata) -> str:
    """
    Returns a title of a tags list.
    """

    return metadata.language.get("tags")


def __get_tags_page_path() -> str:
    """
    Returns a path of a note list: notes/tags.
    """

    path_parts = [constants.NOTES_FOLDER_NAME, "tags"]

    return "/".join(path_parts)


def __get_tags_template_parameters(
    tag_counters: list[dict],
    metadata: metadata_reader.BlogMetadata,
) -> dict[str, typing.Any]:
    page_title = __get_tags_page_title(metadata)
    page_path = __get_tags_page_path()

    result = page_writing_utils.get_html_template_parameters(
        metadata=metadata,
        page_title=page_title,
        page_description="",
        page_path=page_path,
        page_is_editable=False,
    )

    result["tag_counters"] = tag_counters
    result["tags"] = metadata.tags

    return result
