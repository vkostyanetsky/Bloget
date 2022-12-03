#!/usr/bin/env python3

"""
Implementation of a simple web server intended to test building results.
"""

import os
from urllib.parse import urlparse

import flask

from bloget.readers import metadata_reader


def start(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Starts a web server.
    """

    url = metadata.settings.get("url")
    title = metadata.language.get("site_title")
    folder = metadata.paths.get("output")

    app = flask.Flask(title)

    @app.route("/")
    @app.route("/<path:resource_path>")
    def resource(resource_path=None):
        """
        Sends a static file back if it does exist.
        """

        if resource_path is None:
            resource_path = ""

        resource_path = os.path.join(folder, resource_path)

        if os.path.isdir(resource_path):
            resource_path = os.path.join(resource_path, "index.html")

        if not os.path.exists(resource_path):
            flask.abort(404)

        return flask.send_file(resource_path)

    os.chdir(folder)

    parse_result = urlparse(url)

    app.run(host=parse_result.hostname, port=parse_result.port)
