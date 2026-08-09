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
    note_writer,
    notes_list_writer,
    notes_search_index_writer,
    page_404_writer,
    project_writer,
    projects_list_writer,
    robots_writer,
    rss_feed_writer,
    sitemap_writer,
    text_writer,
)


def build_blog(arguments: argparse.Namespace) -> None:
    """
    Initializes blog's data by arguments given, then builds it.
    """

    logging.info("Blog building")

    metadata = metadata_reader.get_metadata(arguments)

    pages = pages_reader.get_pages(metadata, arguments.include_drafts)

    _clear_output(metadata)

    text_writer.write_texts(pages, metadata)

    project_writer.write_projects(pages, metadata)
    projects_list_writer.write_projects_list(pages, metadata)

    note_writer.write_notes(pages, metadata)
    notes_list_writer.write_note_lists(pages, metadata)
    notes_search_index_writer.write_notes_search_index(pages, metadata)

    sitemap_writer.write_sitemap(pages, metadata)
    rss_feed_writer.write_rss_feed(pages, metadata)
    page_404_writer.write_page_404(metadata)
    robots_writer.write_robots(metadata)

    _copy_public(metadata)

    if arguments.webserver:
        logging.info("Starting a web server")
        webserver.start(metadata)


def _check_output_path(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Makes sure the output directory can be cleared without losing a blog's source.
    """

    output_path = os.path.abspath(metadata.paths["output"])

    if os.path.dirname(output_path) == output_path:
        utils.raise_error(
            f"Refusing to use a filesystem root as an output: {output_path}"
        )

    for name in ("pages", "metadata", "public", "templates"):
        source_path = os.path.abspath(metadata.paths[name])

        if source_path == output_path or source_path.startswith(output_path + os.sep):
            utils.raise_error(
                f"Output directory ({output_path}) contains the {name} one "
                f"({source_path}), so clearing it would destroy the source. "
                f"Please choose another output directory."
            )


def _clear_output(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Removes all blog's files and directories which were previously generated.
    """

    logging.info("Clearing output directory")

    _check_output_path(metadata)

    output_path = metadata.paths["output"]

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


def _copy_public(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Copies files from the public directory to the building output directory.
    """

    logging.info("Copying public folder content to the output folder")

    public_path = metadata.paths["public"]
    output_path = metadata.paths["output"]

    for item in os.listdir(public_path):
        source_path = os.path.join(public_path, item)
        target_path = os.path.join(output_path, item)

        utils.copy_file(source_path, target_path)
