import logging
import os

import jinja2

from bloget import utils


def build_page_404(paths: dict, settings: dict, language: dict, templates: jinja2.Environment) -> None:

    logging.info("Building of the page 404 has started.")

    template_parameters = {
        "settings": settings,
        "language": language,
        "page_title": language['page_404_title'],
        "page_path": ""
    }

    file_data = templates.get_template("404.html").render(template_parameters)
    file_path = os.path.join(paths["output"], "404.html")

    utils.make_file(file_path, file_data)

    logging.info("Building of the page 404 is done!")
