#!/usr/bin/env python3

"""
Implementation of the blog's page reader.
"""

import datetime
import os
from dataclasses import dataclass
from typing import Any

from bloget import constants, utils
from bloget.readers import metadata_reader
from bloget.readers.utils import content_parsing_utils


@dataclass
class BlogPageMetadata:
    """
    Container for a page's metadata (data from markdown frontmatter).
    """

    title: str
    description: str
    created: datetime.datetime
    options: list[str]
    stacks: list[str]
    tags: list[str]


@dataclass
class BlogPage:
    """
    Container for a page (note or text).
    """

    folder_path: str
    folder_name: str
    path: str
    text: str

    metadata: BlogPageMetadata
    attachments: list[str]

    @property
    def title(self) -> str:
        return self.metadata.title

    @property
    def description(self) -> str:
        return self.metadata.description

    @property
    def created(self) -> datetime.datetime:
        return self.metadata.created

    @property
    def options(self) -> list[str]:
        return self.metadata.options

    @property
    def tags(self) -> list[str]:
        return self.metadata.tags

    def __repr__(self) -> str:
        return self.folder_path


def get_page(page_folder_path: str, metadata: metadata_reader.BlogMetadata) -> BlogPage:
    """
    Returns object of a blog's page.
    """

    page_folder_name = _get_page_folder_name(page_folder_path, metadata)
    page_path = _get_page_path(page_folder_path, metadata)

    page_info, page_markdown = _read_page_source(page_folder_path)
    page_text = _get_page_text(page_markdown, page_path, metadata)
    page_metadata = _get_page_metadata(page_info)

    page_attachments = _get_page_attachments(page_folder_path)

    return BlogPage(
        page_folder_path,
        page_folder_name,
        page_path,
        page_text,
        page_metadata,
        page_attachments,
    )


def _read_page_source(folder_path: str) -> tuple[dict[str, Any], str]:
    """
    Reads page markdown and extracts frontmatter + body.
    """

    file_path = os.path.join(folder_path, constants.PAGE_TEXT_FILE_NAME)
    return utils.read_markdown_with_frontmatter(file_path)


def _get_page_folder_name(
    folder_path: str, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Determines folder's name.
    """

    pages_path = metadata.paths.get("pages")

    return "" if pages_path == folder_path else os.path.split(folder_path)[1]


def _get_page_path(folder_path: str, metadata: metadata_reader.BlogMetadata) -> str:
    """
    Returns page path by pages_path given.

    For instance:
        pages here: D:\\Blog
        page here: D:\\Blog\\projects\\valhalla
        the function returns: \\projects\\valhalla
    """

    pages_path = metadata.paths.get("pages")
    page_path = folder_path

    folders = []

    while page_path != pages_path:
        page_path_split = os.path.split(page_path)
        page_path = page_path_split[0] if page_path_split else ""

        folders.append(page_path_split[1])

    folders = list(reversed(folders))

    return "/".join(folders)


def _get_page_attachments(folder_path: str) -> list[str]:
    """
    Makes list of attachments in a page folder.
    """

    predefined_file_names = [
        constants.PAGE_TEXT_FILE_NAME,
        constants.PAGE_INFO_FILE_NAME,  # можно потом удалить, если index.yaml больше нигде не останется
    ]

    file_names = os.listdir(folder_path)

    result = []

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name not in predefined_file_names:
            result.append(file_name)

    return result


def _normalize_created(value: Any) -> datetime.datetime:
    """
    Normalizes created field to datetime.
    """

    if value is None:
        return datetime.datetime(1, 1, 1)

    if isinstance(value, datetime.datetime):
        return value

    if isinstance(value, datetime.date):
        return datetime.datetime.combine(value, datetime.time.min)

    raise AssertionError("created must be date or datetime")


def _get_page_metadata(page_info: dict[str, Any]) -> BlogPageMetadata:
    """
    Reads page metadata from markdown frontmatter.
    """
   
    page_title = page_info.get("title")
    assert isinstance(page_title, str)

    page_description = page_info.get("description")
    assert isinstance(page_description, str)

    page_created = _normalize_created(page_info.get("created"))

    page_options = page_info.get("options")
    if page_options is None:
        page_options = []

    page_stacks = page_info.get("stacks")
    if page_stacks is None:
        page_stacks = []

    page_tags = page_info.get("tags")
    if page_tags is None:
        page_tags = []

    return BlogPageMetadata(
        title=page_title,
        description=page_description,
        created=page_created,
        options=page_options,
        stacks=page_stacks,
        tags=page_tags,
    )


def _get_page_text(
    page_markdown: str, page_path: str, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Reads & converts page's content.
    """

    return content_parsing_utils.parse(page_markdown, page_path, metadata)