#!/usr/bin/env python3

"""
Implementation of note pages building functionality.
"""

import logging
import os

from bloget import utils
from bloget.readers import metadata_reader, page_reader, pages_reader
from bloget.writers import page_writer


def build_note_lists():

    def build_page(page_number):

        def get_template_parameters():

            def get_notes_page_url(page_number: int):

                result = config['url'] + '/notes/'

                if selected_tag is not None:
                    result = result + 'tags/' + selected_tag + '/'

                if page_number > 1:
                    result = result + 'page-' + str(page_number) + '/'

                return result

            path = page_parent_path

            if page_dirname != '':
                path = path + page_dirname + '/'

            result = get_standard_template_parameters(
                language['notes'] if selected_tag is None else tags[selected_tag][:1].upper() + tags[selected_tag][
                                                                                                1:],
                language['notes_description'],
                path,
                path,
                False
            )

            result['notes'] = page_notes
            result['tags'] = tags

            result['selected_tag'] = selected_tag
            result['page_parent_path'] = page_parent_path

            if page_number is None:

                result['page_later_url'] = ''
                result['page_earlier_url'] = '' if is_last_page else get_notes_page_url(2)

            else:

                result['page_later_url'] = '' if page_number == 1 else get_notes_page_url(page_number - 1)
                result['page_earlier_url'] = '' if is_last_page else get_notes_page_url(page_number + 1)

            result['hotkey_ctrl_up_url'] = result['page_later_url']
            result['hotkey_ctrl_down_url'] = result['page_earlier_url']

            return result

        if page_number is None:

            page_dirname = ''
            page_dirpath = page_parent_dirpath

        else:

            page_dirname = 'page-' + str(page_number)
            page_dirpath = os.path.join(page_parent_dirpath, page_dirname)

        make_dir(page_dirpath)

        template_parameters = get_template_parameters()
        rendered_template = get_rendered_template(language, templates, 'notes.html', template_parameters)

        write_page(page_dirpath, rendered_template)

    if selected_tag is None:

        notes = pages['notes']

        page_parent_dirpath = paths['project_notes_dirpath']
        page_parent_path = '/notes/'

    else:

        notes = get_notes_by_tag(pages['notes'], selected_tag)

        page_parent_dirpath = os.path.join(paths['project_notes_dirpath'], 'tags', selected_tag)
        page_parent_path = '/notes/tags/' + selected_tag + '/'

    page_number = 1
    page_notes = []
    page_size = 20

    notes_left = len(notes)

    for note in notes:

        page_notes.append(note)
        notes_left -= 1

        if len(page_notes) == page_size or notes_left == 0:

            is_last_page = notes_left == 0

            if page_number == 1:
                build_page(None)

            build_page(page_number)

            page_number += 1
            page_notes = []