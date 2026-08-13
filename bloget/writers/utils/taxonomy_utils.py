#!/usr/bin/env python3

"""
Common methods for taxonomies: tags of notes & stacks of projects.

Both of them are lists of terms in a page's frontmatter, both are shown as
chips, and both have a pre-generated page which lists pages of a term:

    notes/tags/python
    projects/stacks/react
"""

import os
from collections.abc import Callable, Iterable
from urllib.parse import quote

from bloget import utils
from bloget.readers import metadata_reader, page_reader

# A function which returns terms of a page: its tags or its stacks.

TermsGetter = Callable[[page_reader.BlogPage], list[str]]

# A term becomes a folder name in the output directory, so it has to be free
# of characters which a file system (or an URL path) treats in a special way.

FORBIDDEN_CHARACTERS = '\\/:*?"<>|'


def get_note_tags(note: page_reader.BlogPage) -> list[str]:
    """
    Returns tags of a note.
    """

    return note.metadata.tags or []


def get_project_stacks(project: page_reader.BlogPage) -> list[str]:
    """
    Returns stacks of a project.
    """

    return project.metadata.stacks or []


def get_used_terms(
    pages: Iterable[page_reader.BlogPage],
    known_terms: dict[str, str],
    get_page_terms: TermsGetter,
) -> list[str]:
    """
    Returns terms which at least one of the pages given has.

    A term the blog's metadata knows nothing about is skipped: it has no name
    to show, and no chip above a list to filter by, so a page of it would be
    a nameless dead end. Templates leave such a term unclickable.

    The order is the one of the metadata, which is the order of chips above a
    list, so that a build result doesn't depend on a set's iteration order.
    """

    used_terms = {term for page in pages for term in get_page_terms(page)}

    result = [term for term in known_terms if term in used_terms]

    for term in result:
        _check_term(term)

    return result


def get_pages_by_term(
    pages: Iterable[page_reader.BlogPage],
    term: str,
    get_page_terms: TermsGetter,
) -> list[page_reader.BlogPage]:
    """
    Returns pages which have a term given.
    """

    return [page for page in pages if term in get_page_terms(page)]


def get_term_title(known_terms: dict[str, str], term: str) -> str:
    """
    Returns a human-readable name of a term, or the term itself if it is
    missing from the blog's metadata.
    """

    return known_terms.get(term, term)


def get_term_page_path(section_name: str, taxonomy_name: str, term: str) -> str:
    """
    Returns a path of a term's page.

    For instance: notes/tags/python
    """

    return f"{section_name}/{taxonomy_name}/{quote(term, safe='')}"


def get_term_page_url(
    metadata: metadata_reader.BlogMetadata,
    section_name: str,
    taxonomy_name: str,
    term: str,
) -> str:
    """
    Returns an URL of a term's page.

    For instance: https://kostyanetsky.ru/notes/tags/python/
    """

    page_path = get_term_page_path(section_name, taxonomy_name, term)

    return f"{metadata.settings['url']}/{page_path}/"


def get_term_page_urls(
    metadata: metadata_reader.BlogMetadata,
    section_name: str,
    taxonomy_name: str,
    terms: Iterable[str],
) -> dict[str, str]:
    """
    Returns URLs of terms' pages by the terms.

    Templates use the result to turn chips into links, so that URLs of the
    pages are made in one place only.
    """

    return {
        term: get_term_page_url(metadata, section_name, taxonomy_name, term)
        for term in terms
    }


def get_term_folder_path(
    section_folder_path: str, taxonomy_name: str, term: str
) -> str:
    """
    Returns a path to a folder of a term's page.

    For instance: D:/Blog/notes/tags/python

    A term isn't escaped here on purpose: a web server looks for a file by a
    decoded path, so a folder has to be named by the term as it is.
    """

    return os.path.join(section_folder_path, taxonomy_name, term)


def check_folder_names_are_free(
    pages: Iterable[page_reader.BlogPage], taxonomy_name: str, section_name: str
) -> None:
    """
    Makes sure no page takes the folder a taxonomy is going to be written in.
    """

    for page in pages:
        if page.folder_name == taxonomy_name:
            utils.raise_error(
                f'The "{page.folder_path}" page is placed in the folder which '
                f'{section_name} pages of a term use ("{taxonomy_name}"), so '
                f"it would be overwritten. Please rename the page's folder."
            )


def _check_term(term: str) -> None:
    """
    Makes sure a term can be used as a folder name.
    """

    is_correct = (
        bool(term.strip())
        and term not in {os.curdir, os.pardir}
        and not any(character in term for character in FORBIDDEN_CHARACTERS)
    )

    if not is_correct:
        utils.raise_error(
            f'A tag or a stack named "{term}" cannot be used, since a page of '
            f"it has to be written in a folder of the same name. Characters "
            f"which are not allowed: {FORBIDDEN_CHARACTERS}"
        )
