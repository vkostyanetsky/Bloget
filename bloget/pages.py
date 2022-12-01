#!/usr/bin/env python3

"""
Implementation of the classes represent items of blog's data (texts & notes).
"""

import os

from bloget import utils


class BlogPage:
    """
    Basic implementation of blog's page (note or text).
    """

    folder_path: str
    attachments: list
    metadata: dict

    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path
        self.metadata = self.__get_metadata()
        self.attachments = self.__get_attachments()

    def __repr__(self) -> str:
        return self.folder_path

    @staticmethod
    def __get_content_file_name() -> str:
        return "index.md"

    @staticmethod
    def __get_metadata_file_name() -> str:
        return "index.yaml"

    @staticmethod
    def __get_predefined_file_names() -> list:
        return [BlogPage.__get_content_file_name(), BlogPage.__get_metadata_file_name()]

    def __get_metadata(self) -> dict:
        """
        Reads page's metadata.
        """

        file_name = self.__get_metadata_file_name()
        file_path = os.path.join(self.folder_path, file_name)

        return utils.read_yaml_file(file_path)

    def get_content(self) -> str:
        """
        Returns data from a content file.
        """

        return f"{self.folder_path}{self.__get_content_file_name()}"

    def __get_attachments(self) -> list:
        """
        Makes list of attachments in a page folder.
        """

        predefined_file_names = self.__get_predefined_file_names()
        file_names = os.listdir(self.folder_path)

        attachments = []

        for file_name in file_names:

            file_path = os.path.join(self.folder_path, file_name)

            if os.path.isfile(file_path) and file_name not in predefined_file_names:
                attachments.append(file_name)

        return attachments
