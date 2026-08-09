"""
Implementation of RSS feed building functionality.
"""

import datetime
import email.utils
import logging
import os

from bloget import utils
from bloget.readers import metadata_reader, pages_reader

RSS_ITEMS_LIMIT = 10


def write_rss_feed(
    pages: pages_reader.BlogPages,
    metadata: metadata_reader.BlogMetadata,
) -> None:
    """
    Builds & writes rss feed.
    """

    logging.info("RSS FEED BUILDING")

    file_text = _get_file_text(pages, metadata)
    file_path = os.path.join(metadata.paths["output"], "rss.xml")

    utils.make_file(file_path, file_text)

    logging.info("RSS FEED BUILDING DONE")


def _get_file_text(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns content of the rss file.
    """

    template_parameters = {
        "settings": metadata.settings,
        "language": metadata.language,
        "items": _get_rss_items(pages, metadata),
    }

    return metadata.templates.get_template("rss_feed.jinja").render(template_parameters)


def _get_pub_date(created: datetime.datetime) -> str:
    """
    Formats a date as RFC 822 requires, regardless of the current locale.

    A note's date is an UTC one unless its frontmatter specifies an offset
    (for instance, 2024-01-15 10:00:00+04:00).
    """

    return email.utils.format_datetime(created)


def _get_rss_items(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []

    notes = sorted(pages.notes, key=lambda x: x.created, reverse=True)

    for note in notes:
        in_feed = True if note.options is None else "no-rss" not in note.options

        if in_feed:
            item = {
                "title": note.title,
                "link": f"{metadata.settings['url']}/{note.path}",
                "guid": f"note-{note.folder_name}",
                "pub_date": _get_pub_date(note.created),
                "description": note.text,
            }

            items.append(item)

            if len(items) == RSS_ITEMS_LIMIT:
                break

    return items
