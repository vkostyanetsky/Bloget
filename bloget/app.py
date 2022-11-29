#!/usr/bin/env python3

"""
Logging, arguments parser & actions router implementations.
"""

import argparse
import logging
import os

import coloredlogs

from bloget import builder


def main() -> None:
    """
    Main entry point of the application.
    """

    arguments = __get_arguments()

    __setup_logging(arguments)

    if arguments.command == "build":
        builder.build_blog(arguments)
    elif arguments.command == "add":
        pass


def __setup_logging(arguments: argparse.Namespace) -> None:
    """
    Sets up logging feature.
    """

    format_string = "%(asctime)s [%(levelname)s] %(message)s"
    logging_level = logging.DEBUG if arguments.debug else logging.INFO

    logging.basicConfig(level=logging_level, format=format_string)
    coloredlogs.install(level=logging_level, fmt=format_string)


def __get_arguments() -> argparse.Namespace:
    """
    Returns command line arguments.
    """

    parser = argparse.ArgumentParser(description="BLOGET")
    base_parser = argparse.ArgumentParser(add_help=False)

    base_parser.add_argument(
        "--debug", nargs='?', required=False, default=False, const=True
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Action you want the app to do.", required=True
    )

    __add_subparser_for_add_command(subparsers, base_parser)
    __add_subparser_for_build_command(subparsers, base_parser)

    return parser.parse_args()


def __add_subparser_for_add_command(subparsers, base_parser) -> None:
    """
    Adds an arguments subparser for the ADD command.
    """

    subparser = __get_subparser_for_add_command()

    subparsers.add_parser(
        "add", aliases=["a"], help="Add a note", parents=[base_parser, subparser]
    )


def __get_subparser_for_add_command() -> argparse.ArgumentParser:
    """
    Returns an arguments subparser for the ADD command.
    """

    subparser = argparse.ArgumentParser(add_help=False)
    subparser.add_argument(
        "--name", help="A name of a new note", type=str, required=True
    )

    return subparser


def __add_subparser_for_build_command(subparsers, base_parser) -> None:
    """
    Adds an arguments subparser for the BUILD command.
    """

    subparser = __get_subparser_for_build_command()

    subparsers.add_parser(
        "build", aliases=["b"], help="Build blog", parents=[base_parser, subparser]
    )


def __get_subparser_for_build_command() -> argparse.ArgumentParser:
    """
    Returns an arguments subparser for the BUILD command.
    """

    subparser = argparse.ArgumentParser(add_help=False)

    subparser.add_argument(
        "--pages",
        type=str,
        help="input directory with pages (markdown files)",
        default=os.getcwd(),
    )

    subparser.add_argument(
        "--metadata",
        type=str,
        help="input directory with metadata (language, settings, and tags)",
        default=".metadata",
    )

    subparser.add_argument(
        "--skin",
        type=str,
        help="input directory with a skin (templates & assets)",
        default=".skin",
    )

    subparser.add_argument(
        "--output",
        type=str,
        help="output directory to write generated files in",
        required=True,
    )

    subparser.add_argument(
        "--url",
        type=str,
        help="external url of the blog; overrides the 'url' metadata setting",
    )

    return subparser
