import argparse
import os
from pathlib import Path
from typing import Union

from .logger import debug


def find_file(file_path: Union[str, Path]) -> Path:
    path = Path(file_path)
    if path.exists() and os.path.isfile(path):
        return path.absolute()

    home_dir = Path.home()
    home_file_path = home_dir / file_path
    if home_file_path.exists() and os.path.isfile(home_file_path):
        return home_file_path.absolute()

    return home_dir.absolute()


def get_file_contents(file_path: Path) -> str:
    file_path = find_file(file_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_contents = f.read()
            return file_contents
        except UnicodeDecodeError:
            debug(f"There was an issue reading file contents of path: {file_path}.")
            raise argparse.ArgumentTypeError(f"{file_path} is not a valid UTF-8")
    else:
        debug(f"There was an issue reading file contents of path: {file_path}.")
        raise argparse.ArgumentTypeError(f"{file_path} is not a valid file.")
    return ""


def get_history_file_path(shell: str) -> Path:
    home_dir = Path.home()
    if shell == "fish":
        return home_dir / ".local/share/fish/fish_history"
    elif shell == "bash":
        return home_dir / ".bash_history"
    elif shell == "zsh":
        return home_dir / ".zsh_history"
    else:
        return Path.home()
