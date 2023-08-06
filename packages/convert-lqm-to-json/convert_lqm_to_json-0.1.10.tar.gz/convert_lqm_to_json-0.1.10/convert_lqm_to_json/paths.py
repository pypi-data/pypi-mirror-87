from datetime import datetime
from functools import reduce
from glob import glob
from os import getcwd
from os.path import abspath, exists, isdir, isfile, join
from sys import exit


def _reduce_lqm_file_paths(accumulated_paths, arg):
    path = abspath(arg)
    paths = []

    if is_glob_pattern(path) or is_valid_directory_path(path):
        child_paths = glob(path if is_glob_pattern(path) else join(path, "*.lqm"))
        paths = reduce(_reduce_lqm_file_paths, child_paths, [])

    elif is_valid_lqm_file_path(path):
        paths = [path]

    if len(paths) > 0:
        for path in paths:
            if not path in accumulated_paths:
                accumulated_paths.append(path)

    return sorted(accumulated_paths)


def get_default_directory_path():
    return getcwd()


def is_glob_pattern(string):
    return string.find("*") > -1


def is_valid_directory_path(directory_path):
    return exists(directory_path) and isdir(directory_path)


def is_valid_lqm_file_path(file_path):
    return exists(file_path) and isfile(file_path) and file_path.endswith(".lqm")


def resolve_lqm_file_paths(sources=[]):
    if len(sources) == 0:
        sources.append(get_default_directory_path())

    return reduce(_reduce_lqm_file_paths, sources, [])


def resolve_output_directory_path(path=None):
    if path == None:
        return get_default_directory_path()

    return abspath(join(getcwd(), path))


def resolve_output_file_path(directory_path):
    return abspath(
        join(
            directory_path,
            f"lqm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )
    )
