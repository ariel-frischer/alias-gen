import argparse
import os
from argparse import RawTextHelpFormatter
from pathlib import Path

import psutil

from .constants import DEFAULT_SHELL, SUPPORTED_SHELLS
from .file_utils import find_file
from .logger import debug, init_logger

app_desc = """
This script will create bash/zsh/fish shell aliases automatically. You can 
generate a new alias file by following the prompts, or use --stdout to
print results directly in your terminal.
Two types of aliases are suggested, the default alias matches 
all characters in the command while min_alias aims to minimize the length of 
characters. Additionally, min_alias does not necessarily match all characters 
in the command. The freq (frequency) column shows how often this command was 
used. For now, this script only generates aliases for the first word in a 
command. NOTE: Two character commands or less are not processed.\n
By default, fish shell generates abbr (abbreviations) rather than aliases.\n
Full Help Menu:\n
aliaser -h
Example usage with top 40 aliases:\n
aliaser -n 40\n
With stdout and min_alias:\n
aliaser --stdout --use_min_alias
Generate for fish shell:\n
aliaser -s fish
Generate for zsh with custom history file path:\n
aliaser -s zsh -f ./.custom_zsh_history
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description=app_desc,
        epilog="For more information, email me: arielfrischer@gmail.com",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug output.",
    )

    parser.add_argument("-n", type=int, default=30, help="Total number of suggestions default is 30")
    parser.add_argument(
        "-f",
        type=validate_file_exists,
        default="",
        help="Path to history file like ~/.zsh_history if it is not default.",
    )
    parser.add_argument(
        "-s",
        type=validate_shell_args,
        default="",
        help=f"Shell to make aliases for. Supported shells are: {SUPPORTED_SHELLS}.",
    )
    parser.add_argument("--stdout", action="store_true", help="Write output to stdout")
    parser.add_argument("--use_min_alias", action="store_true", help="Will use the min_alias list.")
    args = parser.parse_args()
    init_logger(args)
    return args


def validate_file_exists(file_path: str) -> Path:
    if not file_path:
        return Path.home()
    path = find_file(file_path)
    if not path.exists() or os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{file_path} is not a valid file.")
    return path


def validate_shell_args(shell: str) -> str:
    if not shell:
        shell = detect_shell()
        if shell not in SUPPORTED_SHELLS:
            print(f"This shell: {shell} is not supported, falling back to zsh as default.")
            return DEFAULT_SHELL
    if shell not in SUPPORTED_SHELLS:
        raise argparse.ArgumentTypeError(
            f"Given shell: {shell} is not supported.\nSupported shells are: {SUPPORTED_SHELLS}."
        )
    return shell


def detect_shell_from_pid():
    pid = os.getpid()
    parent = psutil.Process(pid).parent()
    while parent is not None:
        if parent.name() in SUPPORTED_SHELLS:
            return parent.name()
        parent = parent.parent()
    return "unknown"


def detect_shell():
    shell = detect_shell_from_pid()
    debug(f"Detected shell from pid: {shell}")

    if shell not in SUPPORTED_SHELLS:
        shell_path = os.environ.get("SHELL", "")
        debug(f"shell_path: {shell_path}")
        shell = shell_path.split("/")[-1]
    return shell
