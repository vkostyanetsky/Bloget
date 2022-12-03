#!/usr/bin/env python3


"""
Implementation of a class to read blog's data.
"""


import os
from dataclasses import dataclass

from bloget.readers import metadata_reader, page_reader


@dataclass
class BlogPages:
    """
    A container with blog's data to build.
    """

    texts: list[page_reader.BlogPage]
    notes: list[page_reader.BlogPage]


def get_pages(blog_metadata: metadata_reader.BlogMetadata) -> BlogPages:
    """
    Returns a container with blog's pages (texts & notes) to build.
    """

    texts: list[page_reader.BlogPage] = []
    notes: list[page_reader.BlogPage] = []

    pages_path = blog_metadata.paths.get("pages")
    assert isinstance(pages_path, str)

    notes_folder_name = blog_metadata.settings.get("notes_directory")
    assert isinstance(notes_folder_name, str)

    notes_path = os.path.join(pages_path, notes_folder_name)

    for directory, _, files in os.walk(pages_path):

        if "index.yaml" in files:

            is_note = directory.startswith(notes_path)

            page = page_reader.get_page(directory, blog_metadata)

            if is_note:
                notes.append(page)
            else:
                texts.append(page)

    return BlogPages(texts, notes)
