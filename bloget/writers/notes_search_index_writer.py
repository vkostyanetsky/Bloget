#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterable

from bs4 import BeautifulSoup

from bloget import utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers.utils import page_writing_utils


def _html_to_search_text(html: str) -> str:
    """
    Converts HTML to a searchable text.
    """

    soup = BeautifulSoup(html or "", "html.parser")

    # 100% useless

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # separator=" " so that words don't stick together with <br>, </p>, </div>, etc

    text = soup.get_text(separator=" ", strip=True)

    # NBSP (&nbsp;) usually turns into \xa0 - replace and collapse spaces

    text = text.replace("\xa0", " ")
    text = " ".join(text.split())

    return text.lower()


def _build_notes_payload(
    items: Iterable[tuple[page_reader.BlogPage, str]],
) -> list[dict[str, object]]:
    """
    Makes a searchable payload for each note HTML.
    """
    return [
        {
            "html": html,
            "text": _html_to_search_text(html),
            "tags": note.metadata.tags,  # list[str]
        }
        for note, html in items
    ]


def write_notes_search_index(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds notes search index.
    """
    logging.info("Notes search index building")

    notes = page_writing_utils.get_notes(pages.notes)

    rendered = [(note, _get_html(note, metadata)) for note in notes]
    payload = _build_notes_payload(rendered)

    file_text = json.dumps(payload, ensure_ascii=False, indent=2)
    file_path = os.path.join(metadata.paths["output"], "notes.json")
    utils.make_file(file_path, file_text)


def _get_html(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns rendered note.
    """

    template = metadata.templates.get_template("macros.jinja")

    return template.module.note(
        page, metadata.tags, metadata.settings, metadata.language, True
    )
