#!/usr/bin/env python3

"""
The setup and build script for the bloget library.
"""

import setuptools  # type: ignore

from bloget import constants

with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="bloget",
    version=constants.VERSION,
    description="Reads pages & notes from Markdown files and builds a beautiful blog out of it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/Bloget",
    license="MIT",
    python_requires=">=3.10",
    packages=["bloget"],
    install_requires=[
        "beautifulsoup4~=4.11.1",
        "coloredlogs~=15.0.1",
        "Flask~=2.1.1",
        "Jinja2~=3.1.2",
        "Markdown~=3.4.1",
        "PyYAML~=6.0",
    ],
    entry_points={"console_scripts": ["bloget=bloget.app:main"]},
    author="Vlad Kostyanetsky",
    author_email="vlad@kostyanetsky.me",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    keywords="static blog generator",
)
