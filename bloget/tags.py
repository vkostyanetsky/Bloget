#!/usr/bin/env python3


"""
Implementation of general build logic.
"""

import argparse
import logging

from bloget.readers import metadata_reader, pages_reader


def show_tags_list(arguments: argparse.Namespace) -> None:
    """
    Initializes blog's data by arguments given, then builds it.
    """

    logging.info("Blog building")

    metadata = metadata_reader.get_metadata(arguments)

    pages = pages_reader.get_pages(metadata)

    unique_tags = sorted({tag for p in pages.notes for tag in (p.metadata.tags or [])})

    for tag in unique_tags:
        print(tag)
