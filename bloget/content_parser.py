from bs4 import BeautifulSoup
from markdown import markdown
from bloget.readers.metadata_reader import BlogInfo


def parse(content: str, info: BlogInfo) -> str:
    """
    Parses a page's content from Markdown to HTML.
    """

    content = __replace_links_to_social_networks(content, info)
    content = markdown(content)

    return update_html(content)


def __replace_links_to_social_networks(content: str, info: BlogInfo) -> str:
    """
    Replaces links to social networks by applets.
    """

    lines = content.splitlines()

    for (index, line) in enumerate(lines):

        __replace_github_gist_link(lines, index, line, info)

        __replace_youtube_link(lines, index, line, "https://www.youtube.com/watch?v=")
        __replace_youtube_link(lines, index, line, "https://youtu.be/")

    return "\n".join(lines)


def __replace_youtube_link(lines: list, index: int, line: str, marker: str):
    """
    Replaces a link to YouTube by its iframe.
    """

    if line.startswith(marker):

        video_id = line.strip().replace(marker, "")
        template = (
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/{0}" frameborder="0" '
            'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" '
            "allowfullscreen></iframe> "
        )

        lines[index] = template.format(video_id)


def __replace_github_gist_link(lines: list, index: int, line: str, info: BlogInfo):
    """
    Replaces a link to GitHub Gist by its script.
    """

    marker = "https://gist.github.com/"

    if line.startswith(marker):

        gist = line.strip().replace(marker, "").split("/")

        gist_owner = gist[0]
        gist_id = gist[1]

        template = '<script src="https://gist.github.com/{0}/{1}.js">{2}</script>'

        lines[index] = template.format(gist_owner, gist_id, info.language["gist"])


# def get_link(link: str, page: pages.BlogPage, settings: dict):
#
#     result = link
#     is_url = link.startswith('http://') or link.startswith('https://')
#
#     if not is_url:
#
#         prefix = settings['url']
#
#         is_relative_path = not link.startswith('/')
#
#         if is_relative_path:
#             prefix = prefix + page['path']
#
#         result = prefix + link
#
#     return result


def update_html(content: str) -> str:

    soup = BeautifulSoup(content, features="html.parser")

    for tag in soup.find_all("ol"):
        tag["class"] = "measure-wide"

    for tag in soup.find_all("ul"):
        tag["class"] = "measure-wide"

    for tag in soup.find_all("p"):
        tag["class"] = "measure-wide"

    # for tag in soup.find_all("img"):
    #     tag['src'] = get_link(tag['src'])

    for tag in soup.find_all("a"):

        tag["target"] = "_blank"

        if tag.find("img") is None:
            tag["class"] = "link blue dim bb"

        # tag['href'] = get_link(tag['href'])

    return str(soup)
