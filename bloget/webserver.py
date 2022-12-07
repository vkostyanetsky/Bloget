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
    assert isinstance(url, str)

    site_title = metadata.language.get("site_title")
    assert isinstance(site_title, str)

    output_folder = metadata.paths.get("output")
    assert isinstance(output_folder, str)

    app = flask.Flask(site_title)

    @app.route("/")
    @app.route("/<path:resource_path>")
    def resource(resource_path: str | None = None) -> tuple[flask.Response, int]:
        """
        Sends a static file back if it does exist.
        """

        assert isinstance(output_folder, str)

        if resource_path is None:
            resource_path = ""

        resource_path = os.path.join(output_folder, resource_path)

        http_code = 200

        if os.path.isdir(resource_path):
            resource_path = os.path.join(resource_path, "index.html")

        if not os.path.exists(resource_path):
            resource_path = os.path.join(output_folder, "404.html")
            http_code = 404

        if not os.path.exists(resource_path):
            flask.abort(404)

        return flask.send_file(resource_path), http_code

    os.chdir(output_folder)

    parse_result = urlparse(url)

    app.run(host=parse_result.hostname, port=parse_result.port)
