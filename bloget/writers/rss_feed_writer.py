import logging
import os
import html

from bloget import utils
from bloget.readers import metadata_reader, pages_reader


def write_rss_feed(
    pages: pages_reader.BlogPages,
    metadata: metadata_reader.BlogMetadata,
) -> None:

    logging.info("RSS feed building")

    file_text = __get_file_text(pages, metadata)
    file_path = os.path.join(metadata.paths["output"], "rss.xml")

    utils.make_file(file_path, file_text)


def __get_file_text(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns content of the rss file.
    """

    template_parameters = {
        "settings": metadata.settings,
        "language": metadata.language,
        "items": __get_rss_items(pages, metadata),
    }

    return metadata.templates.get_template("rss_feed.xml").render(template_parameters)


def __get_rss_items(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> list[dict[str, str]]:

    items: list[dict[str, str]] = []

    for note in pages.notes:

        in_feed = True if note.options is None else "no-rss" not in note.options

        if in_feed:

            item = {
                "title": html.escape(note.title),
                "link": f"{metadata.settings['url']}/{note.path}",
                "guid": f"note-{note.folder_name}",
                "pub_date": note.created.strftime("%a, %d %b %Y %H:%M:%S +0700"),
                "description": note.text,
            }

            items.append(item)

            if len(items) == 10:
                break

    return items
