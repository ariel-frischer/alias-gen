import os
from pathlib import Path
from typing import Union

import chardet

from .constants import SUPPORTED_FILE_ENCODINGS
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


def get_encoding(file_path: Union[str, Path]) -> str:
    with open(file_path, "rb") as f:
        # Read a portion of the file to detect its encoding
        raw_data = f.read(1024)
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
    return encoding if encoding else "utf-8"


def get_file_contents(file_path: Path) -> str:
    file_path = find_file(file_path)

    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        debug(f"Either path doesnt exist or file_path is not a file: {file_path}.")
        return ""

    detected_encoding = get_encoding(file_path)
    encodings_to_try = [detected_encoding] + SUPPORTED_FILE_ENCODINGS

    for encoding in encodings_to_try:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                file_contents = f.read()
            debug(
                f"Succesfully read file contents of path: {file_path} "
                f"with encoding: {encoding}."
            )
            return file_contents
        except UnicodeDecodeError:
            debug(
                f"Failed to read file contents of path: {file_path} "
                f"with encoding: {encoding}."
            )

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
