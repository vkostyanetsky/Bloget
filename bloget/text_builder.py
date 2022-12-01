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
    logging.debug(f'Output folder path: "{output_folder_path}"')

    utils.make_folder(output_folder_path)

    template_parameters = {
        "text": text.get_content(),
        "page_path": page_path,
        "language": language,
        "settings": settings,
    }

    rendered_template = get_rendered_template(
        templates, "text.html", template_parameters
    )

    write_page(output_folder_path, rendered_template)


def write_page(folder_path: str, content: str):

    filepath = os.path.join(folder_path, "index.html")

    with open(filepath, "w+", encoding="utf-8-sig") as file:
        file.write(content)


def get_rendered_template(templates, filename, parameters: dict):

    template = templates.get_template(filename)

    return template.render(parameters)


# def get_standard_template_parameters(page_title, page_description, page_path, page_base_path, editable=True):
#
#     def get_page_edit_path(page_base_path, editable):
#
#         if editable:
#
#             if config['github_repository'] != '':
#                 result = 'https://github.com/{}/edit/main/pages{}index.md'.format(config['github_repository'],
#                                                                                   page_base_path)
#             else:
#                 result = ''
#
#         else:
#
#             result = ''
#
#         return result
#
#     page_edit_path = get_page_edit_path(page_base_path, editable)
#
#     # print(page_path + ": " + page_edit_path)
#
#     return {
#         'page_title': page_title,
#         'page_description': page_description,
#         'page_path': page_path,
#         'page_edit_path': page_edit_path,
#     }


def get_template_parameters():
    # result = get_standard_template_parameters(
    #     text['metadata']['title'],
    #     text['metadata']['description'],
    #     text['path'],
    #     text['path'],
    #     True
    # )

    result["text"] = text

    return result


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
