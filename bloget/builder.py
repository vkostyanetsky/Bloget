import argparse
import os
import shutil

import jinja2
import logging
from bloget import utils
from bloget import pages, text_builder


def build_blog(arguments: argparse.Namespace) -> None:
    """
    Initializes blog's data by arguments given, then builds it.
    """

    logging.info("Blog building has started.")

    paths = __get_paths(arguments)
    settings = __get_settings(paths, arguments)

    tags = __get_tags(paths)
    language = __get_language(paths)
    templates = __get_templates(paths)

    __clear_output(paths)

    texts, notes = __get_pages(paths, settings)

    text_builder.build_texts(texts, paths, settings, language, templates)


def __build_texts(texts: list, paths: dict) -> None:

    for text in texts:
        text.write(paths["output"])


def __get_pages(paths: dict, settings: dict) -> tuple:
    """
    Returns tuple with texts and notes lists, which contain paths to directories.
    """

    notes_path = os.path.join(paths["pages"], settings["notes_directory"])

    notes = []
    texts = []

    for directory, _, files in os.walk(paths["pages"]):

        if "index.yaml" in files:

            page = pages.BlogPage(directory)

            is_note_page = directory.startswith(notes_path)

            if is_note_page:
                notes.append(page)
            else:
                texts.append(page)

    return texts, notes


def __get_paths(arguments: argparse.Namespace) -> dict:
    """
    Returns paths to various directories required to generate.
    """

    return {
        "metadata": arguments.metadata,
        "pages": arguments.pages,
        "skin": arguments.skin,
        "output": arguments.output,
    }


def __get_settings(paths: dict, arguments: argparse.Namespace) -> dict:
    """
    Returns settings of a blog.
    """

    file_path = os.path.join(paths["metadata"], "settings.yaml")

    settings = utils.read_yaml_file(file_path)

    if arguments.url is not None:
        settings["url"] = arguments.url

    return settings


def __get_tags(paths: dict) -> dict:
    """
    Returns tags of a blog.
    """

    file_path = os.path.join(paths["metadata"], "tags.yaml")

    return utils.read_yaml_file(file_path)


def __get_language(paths: dict) -> dict:
    """
    Returns language of a blog.
    """

    file_path = os.path.join(paths["metadata"], "language.yaml")

    return utils.read_yaml_file(file_path)


def __get_templates(paths: dict) -> jinja2.Environment:
    """
    Returns template of a blog.
    """

    directory_path = os.path.join(paths["skin"], "templates")

    return jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=directory_path))


def __clear_output(paths: dict) -> None:
    """
    Removes all blog's files and directories which were previously generated.
    """

    try:
        for item in os.listdir(paths["output"]):

            protected_files = [".git", "CNAME"]

            if item not in protected_files:

                project_file_path = os.path.join(paths["output"], item)

                if os.path.isfile(project_file_path):
                    os.unlink(project_file_path)
                elif os.path.isdir(project_file_path):
                    shutil.rmtree(project_file_path)

    except IOError:
        utils.raise_error(f"Unable to clear output directory: {paths['output']}")


# def get_page_edit_path(page_path: str, editable: bool, settings: dict):
#
#     result = ""
#
#     if settings['github_repository'] is not None and editable:
#         result = f"https://github.com/{settings['github_repository']}/edit/main/{page_path}index.md"
#
#     return result
#
#
# def __get_template_parameters(page_title: str, page_description: str, page_path: str, page_base_path: str, editable: bool) -> dict:
#     """
#     Returns default template parameters which are applicable to any page.
#     """
#
#     page_edit_path = get_page_edit_path(page_base_path, editable)
#
#     return {
#         'page_title': page_title,
#         'page_description': page_description,
#         'page_path': page_path,
#         'page_edit_path': page_edit_path,
#     }
#
#
# def get_text_template_parameters():
#     """
#     Returns template parameters of a text.
#     """
#
#     result = __get_template_parameters(
#         page_title=text['metadata']['title'],
#         page_description=text['metadata']['description'],
#         page_path=text['path'],
#         page_base_path=text['path'],
#         editable=True
#     )
#
#     result['text'] = text
#
#     return result
#
#
#
#
# def get_rendered_template(language, templates, filename: str, parameters: dict = {}):
#
#     template = templates.get_template(filename)
#
#     parameters['language'] = language
#     parameters['config'] = config
#
#     return template.render(parameters)
#
#
