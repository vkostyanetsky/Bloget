#!/usr/bin/env python3


"""
Implementation of a class to read blog's metadata.
"""

import argparse
import os
from collections import Counter
from dataclasses import dataclass
from typing import Optional

import jinja2

from bloget import utils


@dataclass
class BlogMetadata:
    """
    A class of a container with information about a blog to build.
    """

    paths: dict[str, str]
    settings: dict[str, str]
    language: dict[str, str]
    stacks: dict[str, str]
    tags: dict[str, str]
    templates: jinja2.Environment

    def sort_stacks_by_usage(self, projects: list) -> None:
        """
        Sorts self.stacks in descending order by how often a stack appears in projects' metadata.
        """
        usage = Counter()

        for project in projects:
            project_stacks = project.metadata.stacks or []
            usage.update(set(project_stacks))

        original_index = {
            k: i for i, k in enumerate(self.stacks.keys())
        }  # Stable sort if usage is equal

        sorted_items = sorted(
            self.stacks.items(),
            key=lambda kv: (-usage.get(kv[0], 0), original_index[kv[0]]),
        )

        self.stacks = dict(sorted_items)

    def sort_tags_by_usage(self, notes: list) -> None:
        """
        Sorts self.tags in descending order by how often a tag appears in notes' metadata.
        """
        usage = Counter()

        for note in notes:
            note_tags = note.metadata.tags or []
            usage.update(set(note_tags))

        original_index = {
            k: i for i, k in enumerate(self.tags.keys())
        }  # Stable sort if usage is equal

        sorted_items = sorted(
            self.tags.items(),
            key=lambda kv: (-usage.get(kv[0], 0), original_index[kv[0]]),
        )

        self.tags = dict(sorted_items)


def get_metadata(arguments: argparse.Namespace) -> BlogMetadata:
    """
    Returns a container with information about a blog to build.
    """

    paths = _get_paths(arguments)

    settings = _get_settings(arguments, paths)
    language = _get_language(paths)
    stacks = _get_stacks(paths)
    tags = _get_tags(paths)

    templates = _get_templates(paths)

    return BlogMetadata(paths, settings, language, stacks, tags, templates)


def _get_templates(paths: dict[str, str]) -> jinja2.Environment:
    """
    Returns template of a blog.
    """

    templates_path = paths.get("templates")
    assert isinstance(templates_path, str)

    return jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_path))


def _get_paths(arguments: argparse.Namespace) -> dict[str, Optional[str]]:
    """
    Returns paths to various directories required to generate.
    """

    return {
        "metadata": getattr(arguments, "metadata", ""),
        "pages": getattr(arguments, "pages", ""),
        "assets": getattr(arguments, "assets", ""),
        "templates": getattr(arguments, "templates", ""),
        "output": getattr(arguments, "output", ""),
    }


def _get_settings(
    arguments: argparse.Namespace, paths: dict[str, str]
) -> dict[str, str]:
    """
    Returns settings of a blog.
    """

    metadata_path = _get_metadata_path(paths)
    settings_file_path = os.path.join(metadata_path, "settings.yaml")

    settings = utils.read_yaml_file(settings_file_path)

    url = getattr(arguments, "url", None)

    if url is not None:
        settings["url"] = url

    return settings


def _get_language(paths: dict[str, str]) -> dict[str, str]:
    """
    Returns language of a blog.
    """

    metadata_path = _get_metadata_path(paths)
    language_file_path = os.path.join(metadata_path, "language.yaml")

    return utils.read_yaml_file(language_file_path)


def _get_stacks(paths: dict[str, str]) -> dict[str, str]:
    """
    Returns stacks.
    """

    metadata_path = _get_metadata_path(paths)
    file_path = os.path.join(metadata_path, "stacks.yaml")

    return utils.read_yaml_file(file_path)


def _get_tags(paths: dict[str, str]) -> dict[str, str]:
    """
    Returns tags.
    """

    metadata_path = _get_metadata_path(paths)
    file_path = os.path.join(metadata_path, "tags.yaml")

    return utils.read_yaml_file(file_path)


def _get_metadata_path(paths: dict[str, str]) -> str:
    """
    Returns the path to a folder with metadata.
    """

    metadata_path = paths.get("metadata")
    assert isinstance(metadata_path, str)

    return metadata_path
