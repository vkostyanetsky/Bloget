# в общем скрипт принимает пути к файлам сборки и делает коммиты статусы в этих папках плюс делает сборку... куда-то там
# возможно кстати вообще в темп собирать и удалять при завершении хм, или путь принимать параметром куда собирать

from os import system
from os import chdir
from py_menu import Menu
from webbrowser import open as open_browser
from sys import argv as argv


def display_git_status():

    dirpath = r'.\blog'

    command = r'git -C "{}" pull'.format(dirpath)
    system(command)

    command = r'git -C "{}" status'.format(dirpath)
    system(command)


def execute_git_commit():

    dirpath = r'.\blog'
    message = input("Commit Message: ")

    message_len = len(message)

    if message_len == 0:

        exit('No message entered!')
        
    elif message_len > 50:

        error = 'The message is too long! ({} symbols)'.format(message_len)
        exit(error)    

    command = r'git -C "{}" pull'.format(dirpath)
    system(command)

    command = r'git -C "{}" add .'.format(dirpath)
    system(command)

    command = r'git -C "{}" commit --all --message "{}"'.format(dirpath, message)
    system(command)

    command = r'git -C "{}" push'.format(dirpath)
    system(command)


def build_test_project():

    builder_dirpath = r'D:\Projects\Blogs\BlogBuilder'
    config_filepath = r'.\blog\config-dev.yaml'
    content_dirpath = r'.\blog'
    project_dirpath = argv[1]
        
    command = r'python "{0}\builder.py" --input "{1}" --output "{2}" --config "{3}"'
    command = command.format(builder_dirpath, content_dirpath, project_dirpath, config_filepath)

    system(command)

    open_browser("http://localhost:8000", new=0, autoraise=True)

    chdir(project_dirpath)
    system(r'python -m http.server')    


main_menu = Menu(header="Pick an option!\n")
main_menu.add_option("Display git status", display_git_status)
main_menu.add_option("Execute git commit", execute_git_commit)
main_menu.add_option("Build test project", build_test_project)

main_menu.mainloop()