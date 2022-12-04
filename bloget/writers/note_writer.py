#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

import logging
import os

from bloget import utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers import page_writer


def write_notes(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given note pages.
    """

    logging.info("Notes building...")

    write_notes_by_selected_tag(pages=pages, selected_tag=None, metadata=metadata)

    for selected_tag in metadata.tags:
        write_notes_by_selected_tag(pages=pages, selected_tag=selected_tag, metadata=metadata)

    logging.info("Notes building has been completed!")


def write_notes_by_selected_tag(pages: pages_reader.BlogPages, selected_tag: str | None, metadata: metadata_reader.BlogMetadata) -> None:

    selected_tag_info = "no selected tag" if selected_tag is None else f'selected tag is "{selected_tag}"'

    logging.info(f"Notes building ({selected_tag_info})...")

    for note in pages.notes:
        __write_note(note, metadata, selected_tag)

    logging.info(f"Notes building ({selected_tag_info}) has been completed!")


def __get_output_folder_path(page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata, selected_tag: str) -> str:
    """
    Returns path to note's folder.
    """

    result = os.path.join(metadata.paths["output"], metadata.settings["notes_directory"])

    if selected_tag is not None:
        result = os.path.join(result, "tags", selected_tag)

    return os.path.join(result, page.folder_name)


def __write_note(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata, selected_tag: str | None
) -> None:
    """
    Builds a given text page.
    """

    logging.info('Building a note from "%s"...', page.folder_path)

    output_folder_path = __get_output_folder_path(page, metadata, selected_tag)

    logging.debug('Page path: "%s"', page.path)
    logging.debug('Output folder path: "%s"', output_folder_path)

    file_text = __get_file_text(page, metadata, selected_tag)
    file_path = os.path.join(output_folder_path, "index.html")

    utils.make_folder(output_folder_path)
    utils.make_file(file_path, file_text)

    page_writer.copy_page_attachments(page, output_folder_path)


def get_template_parameters(page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata, selected_tag: str | None) -> dict:

    result = page_writer.get_html_template_parameters(
        metadata=metadata,
        page_title=page.title,
        page_path=page.path,
        page_is_editable=True,
    )

    result['tags'] = metadata.tags
    result['selected_tag'] = selected_tag

    result['text'] = page.text

    # result['note_after_url'] = '' if note_after is None else config['url'] + notes_parent_path + note_after[
    #     'dirname'] + '/'
    # result['note_after_title'] = '' if note_after is None else note_after['metadata']['title']

    # if note_earlier is None:
    #     result['note_earlier_url'] = ''
    # else:
    #     result['note_earlier_url'] = config['url'] + notes_parent_path + note_earlier['dirname'] + '/'

    # result['note_earlier_title'] = '' if note_earlier is None else note_earlier['metadata']['title']

    # result['hotkey_ctrl_right_url'] = result['note_after_url']
    # result['hotkey_ctrl_left_url'] = result['note_earlier_url']

    return result


def __get_file_text(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata, selected_tag: str | None
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = get_template_parameters(page, metadata, selected_tag)
    template_parameters["page_text"] = page.text

    return metadata.templates.get_template("text.html").render(template_parameters)
