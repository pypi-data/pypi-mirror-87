from functools import reduce
from json import dump
from os import mkdir
from sys import argv, exit

from . import __version__
from .memos import extract_data_from_lqm_file
from .paths import (
    get_default_directory_path,
    is_valid_directory_path,
    resolve_lqm_file_paths,
    resolve_output_directory_path,
    resolve_output_file_path,
)

ACCEPT_CURRENT_DIRECTORY_MESSAGE = "Create JSON file in directory [PATH] instead?"

ACCEPT_DIRECTORY_CREATION_MESSAGE = "Directory [PATH] does not exist. Create it now?"

ACCEPT_PROMPT_MESSAGE = "[MESSAGE] [Y/n]: "

ACCEPT_VALUES_CONFIRM = ["Y", "y", ""]

ACCEPT_VALUES_REJECT = ["N", "n"]

FILE_CREATED_MESSAGE = "JSON file containing [COUNT] memos created at [PATH]"

HELP_HEADINGS = [
    "ARGUMENTS",
    "DESCRIPTION",
    "OPTIONS",
    "USAGE",
]

HELP_MESSAGE = """
USAGE
  convert_lqm_to_json [-h] [-o [<...>]] [<source1>] ... [<sourceN>]

ARGUMENTS
  <source>               Paths or glob patterns for resolving .lqm files;
                         defaults to current directory.

OPTIONS
  -o (--output-dir)      Output directory; defaults to current directory.
  -h (--help)            Print this help message.
  -v (--version)         Print application version.

DESCRIPTION
  Convert LG QuickMemo+ .lqm file(s) into single, text-only JSON file.
"""

NO_LQM_FILES_RESOLVED_MESSAGE = "No .lqm files found"

NO_OUTPUT_DIRECTORY_SELECTED_MESSAGE = "No output directory selected."


class AnsiEscapeCodes:
    Bold = "\033[1m"
    Reset = "\033[0m"


def accept(message):
    accepted = None

    while accepted == None:
        user_input = input(ACCEPT_PROMPT_MESSAGE.replace("[MESSAGE]", message))

        if user_input in ACCEPT_VALUES_CONFIRM:
            accepted = True

        elif user_input in ACCEPT_VALUES_REJECT:
            accepted = False

    return accepted


def bold(text):
    return f"{AnsiEscapeCodes.Bold}{text}{AnsiEscapeCodes.Reset}"


def help():
    exit(
        reduce(
            lambda message, heading: message.replace(heading, bold(heading)),
            HELP_HEADINGS,
            HELP_MESSAGE,
        )
    )


def parse_args(args):
    if "-h" in args or "--help" in args:
        help()

    if "-v" in args or "--version" in args:
        version()

    output_dir = None

    while "-o" in args or "--output-dir" in args:
        key = "-o" if "-o" in args else "--output-dir"
        index = args.index(key)
        output_dir = args[index + 1]
        del args[index : index + 2]

    return [resolve_lqm_file_paths(args[:]), resolve_output_directory_path(output_dir)]


def version():
    exit(__version__)


def write_json_file(data, file_path):
    with open(file_path, "w") as file:
        dump(data, file, indent=2)


def main():
    lqm_file_paths, output_directory_path = parse_args(argv[1:])

    if len(lqm_file_paths) == 0:
        exit(NO_LQM_FILES_RESOLVED_MESSAGE)

    if not is_valid_directory_path(output_directory_path):
        if accept(
            ACCEPT_DIRECTORY_CREATION_MESSAGE.replace("[PATH]", output_directory_path)
        ):
            mkdir(output_directory_path)

        else:
            output_directory_path = get_default_directory_path()

            if not accept(
                ACCEPT_CURRENT_DIRECTORY_MESSAGE.replace(
                    "[PATH]", output_directory_path
                )
            ):
                exit(NO_OUTPUT_DIRECTORY_SELECTED_MESSAGE)

    memos = list(
        map(
            lambda lqm_file_path: extract_data_from_lqm_file(lqm_file_path),
            lqm_file_paths,
        )
    )
    memos_count = len(memos)

    output_file_path = resolve_output_file_path(output_directory_path)

    write_json_file(memos, output_file_path)

    output_message = FILE_CREATED_MESSAGE.replace("[COUNT]", str(memos_count)).replace(
        "[PATH]", output_file_path
    )

    if memos_count == 1:
        output_message = output_message.replace("memos", "memo")

    print(output_message)
