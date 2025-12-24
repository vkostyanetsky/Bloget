#!/usr/bin/env python3

"""
Logging, arguments parser & actions router implementations.
"""

import argparse
import logging
import os

import coloredlogs

from bloget import builder, tags


def main() -> None:
    """
    Main entry point of the application.
    """

    arguments = _get_arguments()

    _setup_logging(arguments)

    if arguments.command == "build":

        builder.build_blog(arguments)

    elif arguments.command == "tags":
        if arguments.tags_command == "list":
            tags.show_tags_list(arguments)
        else:
            logging.info("Nothing to do for tags!")

    else:
        logging.info("Nothing to do!")


def _setup_logging(arguments: argparse.Namespace) -> None:
    """
    Sets up logging feature.
    """

    format_string = "%(asctime)s [%(levelname)s] %(message)s"
    logging_level = logging.DEBUG if arguments.debug else logging.INFO

    logging.basicConfig(level=logging_level, format=format_string)
    coloredlogs.install(level=logging_level, fmt=format_string)


def _get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BLOGET")
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        "--debug", nargs="?", required=False, default=False, const=True
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Action you want the app to do.", required=True
    )

    build_command_subparser = __get_subparser_for_build_command()
    build2_command_subparser = __get_subparser_for_build2_command()

    # build
    subparsers.add_parser(
        "build",
        aliases=["b"],
        help="Build blog",
        parents=[base_parser, build_command_subparser],
    )

    # tags
    tags_parser = subparsers.add_parser(
        "tags",
        aliases=["t"],
        help="Manage tags",
        parents=[base_parser],
    )

    tags_subparsers = tags_parser.add_subparsers(
        dest="tags_command", help="Tags action", required=True
    )

    # tags list + build-like args
    tags_subparsers.add_parser(
        "list",
        aliases=["ls"],
        help="List tags",
        parents=[base_parser, build2_command_subparser],
    )

    return parser.parse_args()


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
        help="input directory with metadata (language and settings)",
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

    subparser.add_argument(
        "--webserver",
        help="starts a web server for a blog built",
        nargs="?",
        required=False,
        default=False,
        const=True,
    )

    return subparser


def __get_subparser_for_build2_command() -> argparse.ArgumentParser:
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
        help="input directory with metadata (language and settings)",
        default=".metadata",
    )

    subparser.add_argument(
        "--skin",
        type=str,
        help="input directory with a skin (templates & assets)",
        default=".skin",
    )

    return subparser


if __name__ == "__main__":
    main()
