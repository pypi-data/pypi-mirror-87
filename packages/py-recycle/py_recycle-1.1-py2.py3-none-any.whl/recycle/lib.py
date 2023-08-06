# coding: utf-8

import os
import sys
import re
import datetime
import subprocess

HOME = os.path.expanduser("~")
TRASH_PATH = HOME + "/.Trash"
TRASH_DATETIME_FORMAT = "%Y-%m-%d_%H:%M:%S%f_"
TRASH_REGEX = "^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{8}_[0-9\.]+[A-Z]?$"


def get_current_path():
    try:
        return os.path.abspath(os.getcwd())
    except Exception:
        return None


def my_print(s):
    sys.stdout.write("{}\n".format(s))


def get_path_size_str(file_path):
    return subprocess.check_output(["du", "-sh", file_path]).split()[0].decode("utf-8")


def generate_trash_file_name(file_path):
    return datetime.datetime.now().strftime(TRASH_DATETIME_FORMAT) + get_path_size_str(
        file_path
    )


def directory_exists(directory):
    if not os.path.isdir(directory):
        my_print("{} not exists.".format(directory))
        return False
    return True


def search_files(directory, file_regex):
    files = []
    file_regex = (
        file_regex.replace("(", r"\(")
        .replace(")", r"\)")
        .replace(r"\\(", r"\(")
        .replace(r"\\)", r"\)")
    )
    if not directory_exists(directory):
        return files

    for file_name in os.listdir(directory):
        if re.search(file_regex, file_name):
            files.append(file_name)
    return files


def execute_move(source, destination):
    my_print("mv {} {}".format(source, destination))
    source = re.escape(source)
    destination = re.escape(destination)
    os.system("mv {} {}".format(source, destination))


def remove_empty_dir(absolute_path):
    while os.path.isdir(absolute_path) and not os.listdir(absolute_path):
        os.rmdir(absolute_path)
        absolute_path = absolute_path[: absolute_path.rindex("/")]
        if absolute_path == TRASH_PATH:
            break

def my_input(s):
    try:
        return raw_input(s)
    except:
        return input(s)


def replace_file(file_path):
    if os.path.exists(file_path):
        if (
            "n"
            not in my_input(
                "{} already exists replace it? [y/n]".format(file_path)
            ).lower()
        ):
            trash_file = os.path.join(
                TRASH_PATH + file_path, generate_trash_file_name(file_path)
            )
            execute_move(file_path, trash_file)
            return True
    else:
        return True


def get_absolute_dirs(dirs):
    absolute_dirs = []

    for i in dirs:
        if i == "..":
            absolute_dirs.pop(-1)
        elif absolute_dirs and not (i or absolute_dirs[-1]):
            pass
        else:
            absolute_dirs.append(i)
    return absolute_dirs


def get_parent_dir_and_file_regex(input_arg):

    parent_dir = get_current_path()

    dirs = input_arg.split("/")
    reverse = True

    if dirs:
        if not dirs[0]:
            # use absolute path
            dirs = get_absolute_dirs(dirs)
        else:
            dirs = get_absolute_dirs(parent_dir.split("/") + dirs)
        parent_dir = "/".join(dirs[:-1]) or "/"

    file_regex = dirs[-1] if dirs else input_arg
    return parent_dir, file_regex, reverse


def operations():
    if not os.path.exists(TRASH_PATH):
        os.mkdir(TRASH_PATH)

    for arg in sys.argv[1:]:
        arg = arg.strip().rstrip("/")
        arg = arg[2:] if arg[:2] == "./" else arg
        parent_dir, file_regex, reverse = get_parent_dir_and_file_regex(arg)
        if not arg:
            continue

        if "^" != file_regex[0] and "$" != file_regex[-1]:
            file_regex = "^{}$".format(file_regex)
        yield parent_dir, file_regex, reverse
