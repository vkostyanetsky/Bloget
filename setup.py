#!/usr/bin/env python3

from setuptools import setup
from bloget.constants import VERSION


setup(
    name="bloget",
    version=VERSION,
    description="Reads pages & notes from Markdown files and builds a beautiful blog out of it",
    long_description=open("README.md", encoding="utf-8-sig").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/Bloget",
    license="MIT",
    python_requires=">=3.10",
    packages=["bloget"],
    install_requires=["PyYAML~=6.0"],
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
    keywords="static blog",
)