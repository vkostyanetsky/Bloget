#!/usr/bin/env python3


"""
Implementation of a class to read blog's metadata.
"""


import argparse
import os
from dataclasses import dataclass

from bloget import utils


@dataclass
class BlogMetadata:
    """
    A class of a container with information about a blog to build.
    """

    paths: dict[str, str]
    settings: dict[str, str]
    language: dict[str, str]
    tags: dict[str, str]


def get_metadata(arguments: argparse.Namespace) -> BlogMetadata:
    """
    Returns a container with information about a blog to build.
    """

    paths = __get_paths(arguments)

    settings = __get_settings(arguments, paths)
    language = __get_language(paths)

    tags = __get_tags(paths)

    return BlogMetadata(paths, settings, language, tags)


def __get_paths(arguments: argparse.Namespace) -> dict[str, str]:
    """
    Returns paths to various directories required to generate.
    """

    return {
        "metadata": arguments.metadata,
        "data": arguments.data,
        "skin": arguments.skin,
        "output": arguments.output,
    }


def __get_settings(
    arguments: argparse.Namespace, paths: dict[str, str]
) -> dict[str, str]:
    """
    Returns settings of a blog.
    """

    metadata_path = __get_metadata_path(paths)
    settings_file_path = os.path.join(metadata_path, "settings.yaml")

    settings = utils.read_yaml_file(settings_file_path)

    if arguments.url is not None:
        settings["url"] = arguments.url

    return settings


def __get_language(paths: dict[str, str]) -> dict[str, str]:
    """
    Returns language of a blog.
    """

    metadata_path = __get_metadata_path(paths)
    language_file_path = os.path.join(metadata_path, "language.yaml")

    return utils.read_yaml_file(language_file_path)


def __get_tags(paths: dict[str, str]) -> dict[str, str]:
    """
    Returns tags of a blog.
    """

    metadata_path = __get_metadata_path(paths)
    tags_file_path = os.path.join(metadata_path, "tags.yaml")

    return utils.read_yaml_file(tags_file_path)


def __get_metadata_path(paths: dict[str, str]) -> str:
    """
    Returns the path to a folder with metadata.
    """

    metadata_path = paths.get("metadata")
    assert isinstance(metadata_path, str)

    return metadata_path
