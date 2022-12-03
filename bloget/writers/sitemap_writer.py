import logging
import os

from bloget import utils
from bloget.readers import metadata_reader, page_reader, pages_reader


def write_sitemap(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds & writes the sitemap.xml file.
    """

    logging.info("Sitemap building...")

    file_text = __get_file_text(pages, metadata)
    file_path = os.path.join(metadata.paths["output"], "sitemap.xml")

    utils.make_file(file_path, file_text)

    logging.info("Sitemap building has been done!")


def __get_file_text(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns content of the sitemap file.
    """

    template_parameters = __get_template_parameters(pages, metadata)

    return metadata.templates.get_template("sitemap.xml").render(template_parameters)


def __get_template_parameters(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> dict[str, list[dict[str, str]]]:
    """
    Returns sitemap.xml template parameters.
    """

    links: list[dict[str, str]] = []

    __add_page_links(links, pages.texts, metadata.settings)
    __add_page_links(links, pages.notes, metadata.settings)

    return {"links": links}


def __add_page_links(
    links: list[dict[str, str]],
    pages: list[page_reader.BlogPage],
    settings: dict[str, str],
) -> None:

    for page in pages:

        is_in_sitemap = (
            True if page.options is None else "no-sitemap" not in page.options
        )

        if is_in_sitemap:

            link = {
                "loc": f"{settings['url']}/{page.path}",
                "lastmod": page.created.strftime("%Y-%m-%d"),
            }

            links.append(link)
