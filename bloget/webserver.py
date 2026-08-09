#!/usr/bin/env python3

"""
Implementation of a simple web server intended to test building results.
"""

import logging
import os
import posixpath
from urllib.parse import urlparse

import flask
from werkzeug.utils import safe_join

from bloget import utils
from bloget.readers import metadata_reader

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000

# The server is a preview tool, so it never listens on anything but a loopback.

LOCAL_HOSTNAMES = frozenset({"localhost", "127.0.0.1", "::1"})


def start(metadata: metadata_reader.BlogMetadata) -> None:
    """
    Starts a web server.
    """

    url = metadata.settings.get("url")
    site_title = metadata.language.get("site_title")

    if not isinstance(url, str):
        utils.raise_error('Settings of the blog have no "url" option.')

    if not isinstance(site_title, str):
        utils.raise_error('Language of the blog has no "site_title" option.')

    output_folder = os.path.abspath(metadata.paths["output"])

    app = flask.Flask(str(site_title))

    @app.route("/")
    @app.route("/<path:resource_path>")
    def resource(resource_path: str = "") -> tuple[flask.Response, int]:
        """
        Sends a static file back if it does exist.
        """

        file_path = safe_join(output_folder, resource_path)

        if file_path is not None and os.path.isdir(file_path):
            resource_path = posixpath.join(resource_path, "index.html")
            file_path = safe_join(output_folder, resource_path)

        http_code = 200

        if file_path is None or not os.path.isfile(file_path):
            resource_path = "404.html"
            file_path = os.path.join(output_folder, resource_path)
            http_code = 404

        if not os.path.isfile(file_path):
            flask.abort(404)

        return flask.send_from_directory(output_folder, resource_path), http_code

    host, port = _get_server_address(str(url))

    app.run(host=host, port=port)


def _get_server_address(url: str) -> tuple[str, int]:
    """
    Returns a host & a port for the web server to listen on.

    The blog's URL is used as a source, since it is usually a local one while
    a blog is being tested. An external URL cannot be listened on, so it is
    replaced by the loopback address.
    """

    parse_result = urlparse(url)

    host = parse_result.hostname or DEFAULT_HOST
    port = parse_result.port or DEFAULT_PORT

    if host not in LOCAL_HOSTNAMES:
        logging.warning(
            'The "%s" URL is not a local one, so the web server '
            "is going to listen on %s:%d instead.",
            url,
            DEFAULT_HOST,
            port,
        )

        host = DEFAULT_HOST

    return host, port
