"""
Implementation of text pages building functionality.
"""
import logging
import os

import jinja2

from bloget import pages, utils


def build_texts(
    texts: list,
    paths: dict,
    settings: dict,
    language: dict,
    templates: jinja2.Environment,
) -> None:
    """
    Builds given text pages.
    """

    logging.info("Texts building has started.")

    for text in texts:
        __build_text(text, paths, settings, language, templates)


def __build_text(
    text: pages.BlogPage,
    paths: dict,
    settings: dict,
    language: dict,
    templates: jinja2.Environment,
) -> None:
    """
    Builds a given text page.
    """

    logging.info(f'Building a text from "{text.folder_path}"...')

    page_path = __get_page_path(text, paths["pages"])
    output_folder_path = os.path.join(paths["output"], page_path)

    logging.debug(f'Page path: "{page_path}"')
    logging.debug(f'Output folder path: "{page_path}"')

    utils.make_folder(output_folder_path)


def __get_page_path(page: pages.BlogPage, pages_path: str) -> str:
    """
    Returns page path by pages_path given.

    For instance:
        pages here: D:\\Blog
        page here: D:\\Blog\\projects\\valhalla
        the function returns: \\projects\\valhalla
    """

    page_path = page.folder_path

    folders = []

    while page_path != pages_path:

        page_path_split = os.path.split(page_path)
        page_path = page_path_split[0] if page_path_split else ""

        folders.append(page_path_split[1])

    folders = list(reversed(folders))

    return "/".join(folders)
