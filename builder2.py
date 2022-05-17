import os
import yaml
import shutil
import argparse
import icecream

from jinja2 import Environment
from jinja2 import FileSystemLoader


class BuilderPaths:
    __builder_path: str
    __input_directory_path: str
    __output_directory_path: str

    def __init__(self, input_directory_path: str, output_directory_path: str):
        self.__builder_path = os.path.abspath(os.path.dirname(__file__))
        self.__input_directory_path = input_directory_path
        self.__output_directory_path = output_directory_path

    def get_input_pages_directory_path(self) -> str:
        return os.path.join(self.__input_directory_path, 'pages')

    def get_input_notes_pages_directory_path(self) -> str:
        return os.path.join(
            self.get_input_pages_directory_path(),
            'notes'
        )

    def get_input_tags_file_path(self) -> str:
        return os.path.join(self.__input_directory_path, 'tags.yaml')

    def get_input_language_file_path(self) -> str:
        return os.path.join(self.__input_directory_path, 'language.yaml')

    def get_output_directory_path(self) -> str:
        return self.__output_directory_path

    def get_output_notes_directory_path(self) -> str:
        return os.path.join(self.__output_directory_path, 'notes')

    def get_builder_templates_directory_path(self) -> str:
        return os.path.join(self.__builder_path, 'templates')


class BuilderConfig:
    __config: dict

    def __init__(self, config_path: str):
        self.__config = Builder.read_yaml_file(
            file_path=config_path
        )


class BlogPage:
    __attachments: list = []
    # directory_path: str
    # directory_name: str
    __input_directory_path: str = ''
    __output_directory_path: str = ''

    __paths: BuilderPaths = None
    __config: BuilderConfig = None

    __path: str
    __date: str

    __predefined_file_names: list = ['index.md', 'index.yaml']

    def __init__(self, input_directory_path: str, paths: BuilderPaths, config: BuilderConfig):
        self.__input_directory_path = input_directory_path

        self.output_directory_path = input_directory_path.replace(
            paths.get_input_pages_directory_path(),
            paths.get_output_directory_path()
        )

        self.__paths = paths
        self.__config = config

        self.__set_path()
        self.__set_attachments()

    def __set_path(self):

        self.__path = self.__input_directory_path

        directories = []

        while self.__path != self.__paths.get_input_pages_directory_path():
            split_path = os.path.split(self.__path)
            self.__path = split_path[0]

            directories.append(split_path[1])

        directories = list(reversed(directories))

        if len(directories) > 0:
            self.__path = '/{}/'.format('/'.join(directories))
        else:
            self.__path = '/'

    def __set_attachments(self):

        file_names = os.listdir(self.__input_directory_path)

        for file_name in file_names:

            file_path = os.path.join(self.__input_directory_path, file_name)

            if os.path.isfile(file_path) and file_name not in self.__predefined_file_names:
                self.__attachments.append(file_name)

    @staticmethod
    def is_page(page_directory_path) -> bool:
        return os.path.exists(
            os.path.join(page_directory_path, 'index.yaml')
        )


class Builder:
    __paths: BuilderPaths
    __config: BuilderConfig

    __templates: Environment
    __language: dict
    __tags: dict

    __notes: list = []
    __texts: list = []

    def __init__(self, config_path: str, input_directory_path: str, output_directory_path: str):
        self.__paths = BuilderPaths(
            input_directory_path=input_directory_path,
            output_directory_path=output_directory_path
        )

        self.__config = BuilderConfig(
            config_path=config_path
        )

    def run(self):
        self.__clear_output_directory()

        self.__templates = Environment(
            loader=FileSystemLoader(
                searchpath=self.__paths.get_builder_templates_directory_path()
            )
        )

        self.__language = self.read_yaml_file(
            file_path=self.__paths.get_input_language_file_path()
        )

        self.__tags = self.read_yaml_file(
            file_path=self.__paths.get_input_tags_file_path()
        )

        self.__load_pages()

    def __clear_output_directory(self):
        output_directory = self.__paths.get_output_directory_path()

        for project_file in os.listdir(output_directory):

            protected_files = ['.git', 'CNAME']

            if project_file not in protected_files:

                project_file_path = os.path.join(output_directory, project_file)

                if os.path.isfile(project_file_path):
                    os.unlink(project_file_path)
                elif os.path.isdir(project_file_path):
                    shutil.rmtree(project_file_path)

    def __load_pages(self):

        notes_directory_path = self.__paths.get_input_notes_pages_directory_path()

        directories = os.walk(
            self.__paths.get_input_pages_directory_path()
        )

        for directory in directories:

            directory_path = directory[0]

            if not BlogPage.is_page(directory_path):
                continue

            is_note = directory_path.startswith(notes_directory_path)

            page = BlogPage(
                input_directory_path=directory_path,
                paths=self.__paths,
                config=self.__config
            )

            if is_note:
                self.__notes.append(page)
            else:
                self.__texts.append(page)

        # self.__notes = sorted(
        #     self.__notes,
        #     key=lambda note: note['metadata']['created'],
        #     reverse=True
        # )

    @staticmethod
    def read_yaml_file(file_path):
        with open(file=file_path, encoding='utf-8-sig') as yaml_file:
            result = yaml.safe_load(yaml_file)

        return result


def get_args():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        '--input',
        type=str,
        help='input directory with source data',
        required=True
    )

    args_parser.add_argument(
        '--output',
        type=str,
        help='output directory with result data',
        required=True
    )

    args_parser.add_argument(
        '--config',
        type=str,
        help='configuration file for builder',
        required=True
    )

    return args_parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    Builder(
        config_path=args.config,
        input_directory_path=args.input,
        output_directory_path=args.output
    ).run()
