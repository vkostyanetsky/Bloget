import logging
import os

import jinja2

from bloget import utils


def build_sitemap(
    texts: list, notes: list, paths: dict, settings: dict, templates: jinja2.Environment
) -> None:
    """
    Builds & writes the sitemap.xml file.
    """

    logging.info("Sitemap building has started.")

    template_parameters = __get_template_parameters(texts, notes, settings)

    file_data = templates.get_template("sitemap.xml").render(template_parameters)
    file_path = os.path.join(paths["output"], "sitemap.xml")

    utils.make_file(file_path, file_data)

    logging.info("Sitemap building is done!")


def __get_template_parameters(texts: list, notes: list, settings: dict) -> dict:
    """
    Returns sitemap.xml template parameters.
    """

    urls = []

    __add_urls(urls, texts, settings)
    __add_urls(urls, notes, settings)

    return {"urls": urls}


def __add_urls(urls: list, pages: list, settings: dict):

    for page in pages:

        page_options = page.metadata.get("options")

        is_in_sitemap = (
            True if page_options is None else "no-sitemap" not in page_options
        )

        if is_in_sitemap:

            url = {
                "loc": f"{settings['url']}/{page.page_path}",
                "lastmod": page.metadata["created"].strftime("%Y-%m-%d"),
            }

            urls.append(url)
