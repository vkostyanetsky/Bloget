"""
Implementation of text pages building functionality.
"""
import logging
import os

import jinja2

from bloget import utils


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
    page: pages.BlogPage,
    paths: dict,
    settings: dict,
    language: dict,
    templates: jinja2.Environment,
) -> None:
    """
    Builds a given text page.
    """

    logging.info(f'Building a text from "{page.folder_path}"...')

    output_folder_path = os.path.join(paths["output"], page.page_path)

    logging.debug(f'Page path: "{page.page_path}"')
    logging.debug(f'Output folder path: "{output_folder_path}"')

    utils.make_folder(output_folder_path)

    template_parameters = {
        "language": language,
        "settings": settings,
        "page_title": page.metadata["title"],
        "page_path": page.page_path,
        "page": page,
        "page_edit_url": __get_page_edit_url(page.page_path, settings, True),
    }

    file_text = templates.get_template("text.html").render(template_parameters)
    file_path = os.path.join(output_folder_path, "index.html")

    utils.make_file(file_path, file_text)


def __get_page_edit_url(page_path, settings, editable):

    result = ""

    if editable and settings["github_repository"]:

        parts = [f"https://github.com/{settings['github_repository']}/edit/main"]

        if page_path:
            parts.append(page_path)

        parts.append("index.md")

        result = "/".join(parts)

    return result
