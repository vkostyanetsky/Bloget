#!/usr/bin/env python3


"""
Implementation of general build logic.
"""

import argparse
import logging
import os
import shutil

from bloget import utils, webserver
from bloget.readers import metadata_reader, pages_reader
from bloget.writers import (
    page_404_writer,
    robots_writer,
    rss_feed_writer,
    sitemap_writer,
    text_writer,
    note_writer
)


def build_blog(arguments: argparse.Namespace) -> None:
    """
    Initializes blog's data by arguments given, then builds it.
    """

    logging.info("Blog building...")

    metadata = metadata_reader.get_metadata(arguments)
    pages = pages_reader.get_pages(metadata)

    __clear_output(metadata)

    text_writer.write_texts(pages, metadata)
    note_writer.write_notes(pages, metadata)

    sitemap_writer.write_sitemap(pages, metadata)
    rss_feed_writer.write_rss_feed(pages, metadata)
    page_404_writer.write_page_404(metadata)
    robots_writer.write_robots(metadata)

    __copy_skin_assets(metadata)

    logging.info("Blog building has been done!")

    if arguments.webserver:

        logging.info("Starting a web server...")
        webserver.start(metadata)


def __clear_output(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Removes all blog's files and directories which were previously generated.
    """

    logging.info("Clearing output directory...")

    output_path = metadata.paths.get("output")

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

    logging.info("Clearing output directory has been done!")


def __copy_skin_assets(metadata: metadata_reader.BlogMetadata):
    """
    Copies files from the skin's assets directory to the building output directory.
    """

    logging.info("Copying skin assets...")

    skin_path = metadata.paths.get("skin")
    skin_assets_path = os.path.join(skin_path, "assets")

    output_path = metadata.paths.get("output")

    for item in os.listdir(skin_assets_path):

        source_path = os.path.join(skin_assets_path, item)
        result_path = os.path.join(output_path, item)

        try:

            if os.path.isdir(source_path):
                shutil.copytree(source_path, result_path)
            else:
                shutil.copy2(source_path, result_path)

        except IOError:
            utils.raise_error(f"Unable to copy a file or a folder: {result_path}")

    logging.info("Copying skin assets has been done!")
