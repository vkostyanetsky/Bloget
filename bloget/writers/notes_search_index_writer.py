#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Iterable

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


def _build_notes_payload(html_notes: Iterable[str]) -> list[dict[str, str]]:
    """
    Makes a searchable text for each note HTML.
    """

    return [{"html": h, "text": _html_to_search_text(h)} for h in html_notes]


def write_notes_search_index(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds notes search index.
    """

    logging.info("Notes search index building")

    notes = page_writing_utils.get_notes(pages.notes)
    index = []

    for note in notes:
        index.append(_get_html(note, metadata))

    payload = _build_notes_payload(index)

    file_text = json.dumps(payload, ensure_ascii=False, indent=2)
    file_path = os.path.join(metadata.paths["output"], "notes.json")

    utils.make_file(file_path, file_text)


def _get_html(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns rendered note.
    """

    template = metadata.templates.get_template("macros.html")

    return template.module.render_note(page, metadata.settings, metadata.language, True)
