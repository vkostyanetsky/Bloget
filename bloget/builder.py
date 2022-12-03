#!/usr/bin/env python3


"""
Implementation of general build logic.
"""

import argparse
import logging
import os
import shutil

import jinja2

from bloget import (
    utils,
    webserver
)

from bloget.readers.metadata_reader import BlogInfo
from bloget.readers.pages_reader import BlogData

from bloget.writers import sitemap_builder, text_builder, page_404_builder, rss_feed_builder


def build_blog(arguments: argparse.Namespace) -> None:
    """
    Initializes blog's data by arguments given, then builds it.
    """

    logging.info("Building has started.")

    info = __get_info(arguments)
    data = __get_data(info)
    skin = __get_skin(info)

    __clear_output(info)

    text_builder.build_texts(info, skin, data)
    sitemap_builder.build_sitemap(info, skin, data)
    rss_feed_builder.build_rss_feed(info, skin, data)
    page_404_builder.build_page_404(info, skin, data)

    logging.info("Building is done!")

    __copy_assets(info)

    if arguments.webserver:
        webserver.start(
            url=settings["url"], title=language["site_title"], folder=paths["output"]
        )


def __get_info(arguments: argparse.Namespace) -> BlogInfo:

    paths = __get_paths(arguments)
    settings = __get_settings(paths, arguments)

    tags = __get_tags(paths)
    language = __get_language(paths)

    return BlogInfo(settings, language, paths, tags)


def __get_data(info: BlogInfo) -> BlogData:

    return BlogData(info)

def __get_skin(info: BlogInfo) -> jinja2.Environment:
    """
    Returns template of a blog.
    """

    skin_path = info.paths.get("skin")
    skin_templates_path = os.path.join(skin_path, "templates")

    return jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=skin_templates_path))


def __copy_assets(info: BlogInfo):

    skin_path = info.paths.get("skin")
    skin_assets_path = os.path.join(skin_path, "assets")

    output_path = info.paths.get("output")

    for item in os.listdir(skin_assets_path):

        source_path = os.path.join(skin_assets_path, item)
        result_path = os.path.join(output_path, item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, result_path)
        else:
            shutil.copy2(source_path, result_path)


def __clear_output(info: BlogInfo) -> None:
    """
    Removes all blog's files and directories which were previously generated.
    """

    output_path = info.paths.get("output")

    try:
        for item in os.listdir(output_path):

            protected_files = [".git", "CNAME"]

            if item not in protected_files:

                project_file_path = os.path.join(output_path, item)

                if os.path.isfile(project_file_path):
                    os.unlink(project_file_path)
                elif os.path.isdir(project_file_path):
                    shutil.rmtree(project_file_path)

    except IOError:
        utils.raise_error(f"Unable to clear output directory: {output_path}")


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
