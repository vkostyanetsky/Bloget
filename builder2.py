import os
import yaml
import shutil
import argparse
import icecream

from jinja2 import Environment
from jinja2 import FileSystemLoader


# class BlogPage:
#     __attachments: list = []
#     __input_directory_path: str = ''
#     __output_directory_path: str = ''
#
#     __path: str
#     __date: str
#
#     __predefined_file_names: list = ['index.md', 'index.yaml']
#
#     def __init__(self, input_directory_path: str, paths: BuilderPaths, config: BuilderConfig):
#         self.__input_directory_path = input_directory_path
#
#         self.output_directory_path = input_directory_path.replace(
#             paths.get_input_pages_directory_path(),
#             paths.get_output_directory_path()
#         )
#
#         self.__paths = paths
#         self.__config = config
#
#         self.__set_path()
#         self.__set_attachments()
#
#     def __set_path(self):
#
#         self.__path = self.__input_directory_path
#
#         directories = []
#
#         while self.__path != self.__paths.get_input_pages_directory_path():
#             split_path = os.path.split(self.__path)
#             self.__path = split_path[0]
#
#             directories.append(split_path[1])
#
#         directories = list(reversed(directories))
#
#         if len(directories) > 0:
#             self.__path = '/{}/'.format('/'.join(directories))
#         else:
#             self.__path = '/'
#
#     def __set_attachments(self):
#
#         file_names = os.listdir(self.__input_directory_path)
#
#         for file_name in file_names:
#
#             file_path = os.path.join(self.__input_directory_path, file_name)
#
#             if os.path.isfile(file_path) and file_name not in self.__predefined_file_names:
#                 self.__attachments.append(file_name)


# class BlogPageBuilder:
#     __paths: BuilderPaths = None
#     __config: BuilderConfig = None
#
#     @staticmethod
#     def is_page(page_directory_path) -> bool:
#         return os.path.exists(
#             os.path.join(page_directory_path, 'index.yaml')
#         )

class BlogBuilderPaths:

    __application_path: str = ''
    __templates_path: str = ''

    __input_path: str = ''
    __input_tags_path: str = ''
    __input_language_path: str = ''
    __input_pages_path: str = ''
    __input_notes_path: str = ''

    __output_path: str = ''
    __output_notes_path: str = ''

    def __init__(self, input_path: str, output_path: str):
        self.__application_path = os.path.abspath(os.path.dirname(__file__))
        self.__templates_path = os.path.join(self.__application_path, 'templates')

        self.__input_path = input_path
        self.__input_tags_path = os.path.join(self.__input_path, 'tags.yaml')
        self.__input_language_path = os.path.join(self.__input_path, 'language.yaml')
        self.__input_pages_path = os.path.join(self.__input_path, 'pages')
        self.__input_notes_path = os.path.join(self.__input_pages_path, 'notes')

        self.__output_path = output_path
        self.__output_notes_path = os.path.join(self.__output_path, 'notes')

    @property
    def application_path(self) -> str:
        return self.__application_path

    @property
    def templates_path(self) -> str:
        return self.__templates_path

    @property
    def input_path(self) -> str:
        return self.__input_path

    @property
    def input_tags_path(self) -> str:
        return self.__input_tags_path

    @property
    def input_language_path(self) -> str:
        return self.__input_language_path

    @property
    def input_pages_path(self) -> str:
        return self.__input_pages_path

    @property
    def input_notes_path(self) -> str:
        return self.__input_notes_path

    @property
    def output_path(self) -> str:
        return self.__output_path

    @property
    def output_notes_path(self) -> str:
        return self.__output_notes_path


class BlogBuilderConfig:

    __url: str = ''
    __language_code: str = ''
    __mirror_url: str = ''
    __mirror_language_code: str = ''
    __github_repository: str = ''

    def __init__(self, config_path):

        def get_config_value(attribute_name):

            attribute_value = config.get(attribute_name)

            return attribute_value if type(attribute_value) is str else ''

        config = BlogBuilderApplication.read_yaml_file(config_path)

        self.__url = get_config_value('url')
        self.__language_code = get_config_value('language_code')
        self.__mirror_url = get_config_value('mirror_url')
        self.__mirror_language_code = get_config_value('mirror_language_code')
        self.__github_repository = get_config_value('github_repository')

    @property
    def url(self) -> str:
        return self.__url

    @property
    def language_code(self) -> str:
        return self.__language_code

    @property
    def mirror_url(self) -> str:
        return self.__mirror_url

    @property
    def mirror_language_code(self) -> str:
        return self.__mirror_language_code

    @property
    def github_repository(self) -> str:
        return self.__github_repository


class BlogBuilderApplication:
    __config: BlogBuilderConfig
    __paths: BlogBuilderPaths
    __language: dict = {}
    __tags: dict = {}
    __templates: Environment
    __notes: list = []
    __texts: list = []

    def __init__(self, input_path: str, output_path: str, config_path: str) -> None:

        self.__paths = BlogBuilderPaths(input_path=input_path, output_path=output_path)
        self.__config = BlogBuilderConfig(config_path=config_path)

        self.__set_language()
        self.__set_tags()
        self.__set_templates()

    def __set_language(self) -> None:
        self.__language = self.read_yaml_file(file_path=self.__paths.input_language_path)

    def __set_tags(self) -> None:
        self.__tags = self.read_yaml_file(file_path=self.__paths.input_tags_path)

    def __set_templates(self) -> None:
        self.__templates = Environment(
            loader=FileSystemLoader(searchpath=self.__paths.templates_path)
        )

    def run(self) -> None:
        self.__clear_output_directory()
        self.__load_pages()

    def __clear_output_directory(self) -> None:
        output_directory = self.__paths.output_path

        for project_file in os.listdir(output_directory):

            protected_files = ['.git', 'CNAME']

            if project_file not in protected_files:

                project_file_path = os.path.join(output_directory, project_file)

                if os.path.isfile(project_file_path):
                    os.unlink(project_file_path)
                elif os.path.isdir(project_file_path):
                    shutil.rmtree(project_file_path)

    def __load_pages(self) -> None:

        notes_path = self.__paths.input_notes_path

        directories = os.walk(self.__paths.input_pages_path)

        for directory in directories:

            directory_path = directory[0]

            # if not BlogPage.is_page(directory_path):
            #     continue

            # is_note = directory_path.startswith(notes_directory_path)

            # page = BlogPage(
            #     input_directory_path=directory_path,
            #     paths=self.__paths,
            #     config=self.__config
            # )
            #
            # if is_note:
            #     self.__notes.append(page)
            # else:
            #     self.__texts.append(page)

        # self.__notes = sorted(
        #     self.__notes,
        #     key=lambda note: note['metadata']['created'],
        #     reverse=True
        # )

    @staticmethod
    def read_yaml_file(file_path) -> dict:
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
    BlogBuilderApplication(
        input_path=args.input,
        output_path=args.output,
        config_path=args.config
    ).run()
