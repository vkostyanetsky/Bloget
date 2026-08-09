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

# A stub for pages whose frontmatter has no creation date.

UNKNOWN_DATE = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


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
        """
        Shortcut for the page's title.
        """

        return self.metadata.title

    @property
    def description(self) -> str:
        """
        Shortcut for the page's description.
        """

        return self.metadata.description

    @property
    def created(self) -> datetime.datetime:
        """
        Shortcut for the page's creation date.
        """

        return self.metadata.created

    @property
    def options(self) -> list[str]:
        """
        Shortcut for the page's options.
        """

        return self.metadata.options

    @property
    def tags(self) -> list[str]:
        """
        Shortcut for the page's tags.
        """

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
    page_metadata = _get_page_metadata(page_info, page_folder_path)

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
        the function returns: projects/valhalla
    """

    pages_path = metadata.paths["pages"]

    try:
        page_path = os.path.relpath(folder_path, pages_path)
    except ValueError:  # different drives on Windows
        page_path = ".."

    if page_path.startswith(".."):
        utils.raise_error(
            f'Page folder "{folder_path}" is outside of the pages one: {pages_path}'
        )

    return "" if page_path == os.curdir else page_path.replace(os.sep, "/")


def _get_page_attachments(folder_path: str) -> list[str]:
    """
    Makes list of attachments in a page folder.
    """

    predefined_file_names = [
        constants.PAGE_TEXT_FILE_NAME,
        # можно потом удалить, если index.yaml больше нигде не останется:
        constants.PAGE_INFO_FILE_NAME,
    ]

    file_names = os.listdir(folder_path)

    result = []

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name not in predefined_file_names:
            result.append(file_name)

    return result


def _normalize_created(value: Any, folder_path: str) -> datetime.datetime:
    """
    Normalizes created field to a time zone aware datetime.

    A date without an offset is considered to be an UTC one. Keeping every date
    aware makes pages comparable to each other, no matter how their authors
    wrote the dates down.
    """

    if value is None:
        return UNKNOWN_DATE

    if isinstance(value, datetime.datetime):
        created = value

    elif isinstance(value, datetime.date):
        created = datetime.datetime.combine(value, datetime.time.min)

    else:
        utils.raise_error(
            f'Frontmatter of the page "{folder_path}" has a "created" field '
            f"which is neither a date nor a date & time: {value!r}"
        )

        return UNKNOWN_DATE

    if created.tzinfo is None:
        created = created.replace(tzinfo=datetime.timezone.utc)

    return created


def _get_string_field(
    page_info: dict[str, Any], field_name: str, folder_path: str
) -> str:
    """
    Reads a mandatory string field of a page's frontmatter.
    """

    value = page_info.get(field_name)

    if not isinstance(value, str):
        utils.raise_error(
            f'Frontmatter of the page "{folder_path}" has no '
            f'"{field_name}" field, or it is not a text one.'
        )

    return str(value)


def _get_page_metadata(page_info: dict[str, Any], folder_path: str) -> BlogPageMetadata:
    """
    Reads page metadata from markdown frontmatter.
    """

    page_title = _get_string_field(page_info, "title", folder_path)
    page_description = _get_string_field(page_info, "description", folder_path)

    page_created = _normalize_created(page_info.get("created"), folder_path)

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
