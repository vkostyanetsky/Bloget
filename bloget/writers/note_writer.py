#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

import logging
import os

from bloget import utils, constants
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers import page_writer


def write_notes(
    pages: pages_reader.BlogPages, metadata: metadata_reader.BlogMetadata
) -> None:
    """
    Builds given note pages.
    """

    logging.info("Notes building...")

    __write_notes_by_selected_tag(pages=pages, selected_tag=None, metadata=metadata)

    for selected_tag in metadata.tags:
        __write_notes_by_selected_tag(pages=pages, selected_tag=selected_tag, metadata=metadata)

    logging.info("Notes building has been completed!")


def __write_notes_by_selected_tag(pages: pages_reader.BlogPages, selected_tag: str | None, metadata: metadata_reader.BlogMetadata) -> None:

    selected_tag_comment = __get_selected_tag_comment(selected_tag)

    logging.info(f"Notes building ({selected_tag_comment})...")

    for page in pages.notes:

        if selected_tag is None or selected_tag in page.tags:
            __write_note(page, metadata, selected_tag)


def __write_note(
    page: page_reader.BlogPage,
    metadata: metadata_reader.BlogMetadata, selected_tag: str | None
) -> None:
    """
    Builds a given text page.
    """

    tag_comment = __get_selected_tag_comment(selected_tag)
    logging.info('Building a note "%s" (%s)...', page.folder_name, tag_comment)

    output_folder_path = __get_output_folder_path(page, metadata, selected_tag)
    logging.debug('Output folder path: "%s"', output_folder_path)

    file_text = __get_file_text(page, metadata, selected_tag)
    file_path = os.path.join(output_folder_path, "index.html")

    utils.make_folder(output_folder_path)
    utils.make_file(file_path, file_text)

    page_writer.copy_page_attachments(page, output_folder_path)


def __get_file_text(
    page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata, selected_tag: str | None
) -> str:
    """
    Returns template parameters for the note.html file.
    """

    template_parameters = __get_template_parameters(page, metadata, selected_tag)
    template_parameters["page_text"] = page.text

    return metadata.templates.get_template("text.html").render(template_parameters)


def __get_template_parameters(page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata, selected_tag: str | None) -> dict:

    result = page_writer.get_html_template_parameters(
        metadata=metadata,
        page_title=page.title,
        page_path=page.path,
        page_is_editable=True,
    )

    result['tags'] = metadata.tags
    result['selected_tag'] = selected_tag

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


def __get_output_folder_path(page: page_reader.BlogPage, metadata: metadata_reader.BlogMetadata, selected_tag: str) -> str:
    """
    Returns path to note's folder.
    """

    result = os.path.join(metadata.paths["output"], constants.NOTES_FOLDER_NAME)

    if selected_tag is not None:
        result = os.path.join(result, "tags", selected_tag)

    return os.path.join(result, page.folder_name)


def __get_selected_tag_comment(selected_tag: str | None) -> str:
    """
    Returns a comment for a tag selected.
    """

    return "no selected tag" if selected_tag is None else f'selected tag is "{selected_tag}"'
