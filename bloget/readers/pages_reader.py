#!/usr/bin/env python3


"""
Implementation of a class to read blog's data.
"""


import os
from dataclasses import dataclass

from bloget import constants
from bloget.readers import metadata_reader, page_reader


@dataclass
class BlogPages:
    """
    A container with blog's data to build.
    """

    texts: list[page_reader.BlogPage]
    notes: list[page_reader.BlogPage]
    projects: list[page_reader.BlogPage]


def get_pages(blog_metadata: metadata_reader.BlogMetadata) -> BlogPages:
    """
    Returns a container with blog's pages (texts & notes) to build.
    """

    texts: list[page_reader.BlogPage] = []
    notes: list[page_reader.BlogPage] = []
    projects: list[page_reader.BlogPage] = []

    pages_path = blog_metadata.paths.get("pages")
    assert isinstance(pages_path, str)

    notes_path = _notes_path(pages_path)
    projects_path = _projects_path(pages_path)

    for directory, _, files in os.walk(pages_path):
        if "index.yaml" in files:
            is_note = directory.startswith(notes_path)
            is_project = directory.startswith(projects_path)

            page = page_reader.get_page(directory, blog_metadata)

            if is_note:
                notes.append(page)
            elif is_project:
                projects.append(page)
            else:
                texts.append(page)

    blog_metadata.sort_tags_by_usage(notes)
    blog_metadata.sort_stacks_by_usage(projects)
    
    return BlogPages(texts, notes, projects)


def _notes_path(pages_path: str) -> str:
    notes_folder_name = constants.NOTES_FOLDER_NAME
    assert isinstance(notes_folder_name, str)

    return os.path.join(pages_path, notes_folder_name)


def _projects_path(pages_path: str) -> str:
    projects_folder_name = constants.PROJECTS_FOLDER_NAME
    assert isinstance(projects_folder_name, str)

    return os.path.join(pages_path, projects_folder_name)