#!/usr/bin/env python3

"""
Content parser for texts & notes.
"""

from bs4 import BeautifulSoup
from markdown import markdown

from bloget.readers import metadata_reader


def parse(content: str, page_path: str, metadata: metadata_reader.BlogMetadata) -> str:
    """
    Parses a page's content from Markdown to HTML.
    """

    content = _replace_links_to_social_networks(content)
    content = markdown(content)

    return _update_internal_links(content, page_path, metadata)


def _replace_links_to_social_networks(content: str) -> str:
    """
    Replaces links to social networks by applets.
    """

    lines = content.splitlines()

    for index, line in enumerate(lines):
        _replace_github_gist_link(lines, index, line)

        _replace_youtube_link(lines, index, line, "https://www.youtube.com/watch?v=")
        _replace_youtube_link(lines, index, line, "https://youtu.be/")

    return "\n".join(lines)


def _replace_youtube_link(lines: list[str], index: int, line: str, marker: str) -> None:
    """
    Replaces a link to YouTube by its iframe.
    """

    if line.startswith(marker):
        video_id = line.strip().replace(marker, "")
        template = (
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/{0}" '
            'frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; '
            'picture-in-picture" allowfullscreen></iframe> '
        )

        lines[index] = template.format(video_id)


def _replace_github_gist_link(lines: list[str], index: int, line: str) -> None:
    """
    Replaces a link to GitHub Gist by its script.
    """

    marker = "https://gist.github.com/"

    if line.startswith(marker):
        gist = line.strip().replace(marker, "").split("/")

        gist_owner = gist[0]
        gist_id = gist[1]

        template = '<script src="https://gist.github.com/{0}/{1}.js">{2}</script>'

        lines[index] = template.format(gist_owner, gist_id, "Gist")


def get_internal_link(
    link: str, page_path: str, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Returns full link to a current page if a link is relative.
    """

    def delete_slashes(item: str):
        return item.strip("/")

    result = link
    is_url = link.startswith("http://") or link.startswith("https://")

    if not is_url:
        link_parts = [metadata.settings["url"]]

        is_relative_path = not link.startswith("/")

        if is_relative_path:
            link_parts.append(page_path)

        link_parts.append(link)

        link_parts = map(delete_slashes, link_parts)

        result = "/".join(link_parts)

    return result


def _update_internal_links(
    content: str, page_path: str, metadata: metadata_reader.BlogMetadata
) -> str:
    """
    Implementation of a full cycle of updating page's html.
    """

    soup = BeautifulSoup(content, features="html.parser")

    for tag in soup.find_all("img"):
        tag["src"] = get_internal_link(tag["src"], page_path, metadata)

    for tag in soup.find_all("a"):
        tag["target"] = "_blank"
        tag["href"] = get_internal_link(tag["href"], page_path, metadata)

    return str(soup)
