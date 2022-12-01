#!/usr/bin/env python3

"""
Implementation of a simple web server intended to test building results.
"""

import os
from urllib.parse import urlparse

import flask

from bloget import constants


async def start(paths, settings):
    """
    Starts a web server.
    """

    app = flask.Flask(constants.TITLE)

    @app.route("/")
    @app.route("/<path:resource_path>")
    def resource(resource_path=None):
        """
        Sends a static file back if it does exist.
        """

        if resource_path is None:
            resource_path = ""

        resource_path = os.path.join(paths["output"], resource_path)

        if os.path.isdir(resource_path):
            resource_path = os.path.join("index.html")

        if not os.path.exists(resource_path):
            flask.abort(404)

        return flask.send_file(resource_path)

    os.chdir(paths["output"])

    parse_result = urlparse(settings["url"])

    app.run(host=parse_result.hostname, port=parse_result.port)
