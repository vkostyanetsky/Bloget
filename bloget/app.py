#!/usr/bin/env python3

"""
Logging, arguments parser & actions router implementations.
"""

import argparse
import logging

import coloredlogs

from bloget import builder


def main() -> None:
    """
    Main entry point of the application.
    """

    __setup_logging()

    arguments = __get_arguments()

    if arguments.command == "build":
        builder.build_blog(arguments)
    elif arguments.command == "add":
        pass


def __setup_logging() -> None:
    """
    Sets up logging feature.
    """

    format_string = "%(asctime)s [%(levelname)s] %(message)s"

    logging.basicConfig(level=logging.INFO, format=format_string)
    coloredlogs.install(level=logging.INFO, fmt=format_string)


def __get_arguments() -> argparse.Namespace:
    """
    Returns command line arguments.
    """

    parser = argparse.ArgumentParser(description="BLOGET")
    base_parser = argparse.ArgumentParser(add_help=False)

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
        default="",
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
