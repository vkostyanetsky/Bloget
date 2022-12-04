#!/usr/bin/env python3

"""
Implementation of the blog's page reader.
"""

import datetime
import os
from dataclasses import dataclass

from bloget import constants, content_parser, utils
from bloget.readers import metadata_reader


@dataclass
class BlogPage:
    """
    Implementation of blog's page (note or text).
    """

    folder_path: str
    folder_name: str
    path: str
    text: str

    title: str
    description: str
    created: datetime.datetime
    options: list[str]
    tags: list[str]

    attachments: list[str]

    def __repr__(self) -> str:
        return self.folder_path


def get_page(page_folder_path: str, metadata: metadata_reader.BlogMetadata) -> BlogPage:
    """
    Returns object of a blog's page.
    """

    page_folder_name = __get_page_folder_name(page_folder_path, metadata)

    page_path = __get_page_path(page_folder_path, metadata)
    page_text = __get_page_text(page_folder_path, page_path, metadata)

    page_info = __get_page_info(page_folder_path)

    page_title = page_info.get("title")
    page_description = page_info.get("description")

    page_created = page_info.get("created")
    if page_created is None:
        page_created = datetime.datetime(1, 1, 1)

    page_options = page_info.get("options")
    if page_options is None:
        page_options = []

    page_tags = page_info.get("tags")
    if page_tags is None:
        page_tags = []

    page_attachments = __get_page_attachments(page_folder_path)

    return BlogPage(
        page_folder_path,
        page_folder_name,
        page_path,
        page_text,
        page_title,
        page_description,
        page_created,
        page_options,
        page_tags,
        page_attachments,
    )


def __get_page_folder_name(
    folder_path: str, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Determines folder's name.
    """

    pages_path = metadata.paths.get("pages")

    return "" if pages_path == folder_path else os.path.split(folder_path)[1]


def __get_page_path(folder_path: str, metadata: metadata_reader.BlogMetadata) -> str:
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


def __get_page_attachments(folder_path: str) -> list[str]:
    """
    Makes list of attachments in a page folder.
    """

    predefined_file_names = [
        constants.PAGE_TEXT_FILE_NAME,
        constants.PAGE_INFO_FILE_NAME,
    ]

    file_names = os.listdir(folder_path)

    result = []

    for file_name in file_names:

        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name not in predefined_file_names:
            result.append(file_name)

    return result


def __get_page_info(folder_path: str) -> dict[str, str | list[str]]:
    """
    Reads page's information.
    """

    file_path = os.path.join(folder_path, constants.PAGE_INFO_FILE_NAME)

    return utils.read_yaml_file(file_path)


def __get_page_text(
    folder_path: str, page_path: str, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Reads & converts page's content.
    """

    file_path = os.path.join(folder_path, constants.PAGE_TEXT_FILE_NAME)

    with open(file_path, encoding=constants.ENCODING) as file:
        result = file.read()

    return content_parser.parse(result, page_path, metadata)
