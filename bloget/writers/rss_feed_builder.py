import logging
import os

import jinja2

from bloget import utils


def build_rss_feed(
    notes: list,
    paths: dict,
    settings: dict,
    language: dict,
    templates: jinja2.Environment,
) -> None:

    logging.info("RSS feed building has started.")

    template_parameters = __get_template_parameters(notes, settings, language)

    file_data = templates.get_template("rss.xml").render(template_parameters)
    file_path = os.path.join(paths["output"], "rss.xml")

    utils.make_file(file_path, file_data)

    logging.info("RSS feed building is done!")


def __get_template_parameters(notes: list, settings: dict, language: dict) -> dict:

    items = []

    for note in notes:

        options = note.metadata.get("options")
        in_feed = True if options is None else "no-rss" not in options

        if in_feed:

            item = {
                "title": note.metadata["title"],
                "link": f"{settings['url']}/{note.page_path}",
                "guid": f"note-{note.folder_name}",
                "pub_date": note.metadata["created"].strftime(
                    "%a, %d %b %Y %H:%M:%S +0700"
                ),
                "description": note.content,
            }

            items.append(item)

            if len(items) == 10:
                break

    return {"items": items, "settings": settings, "language": language}
