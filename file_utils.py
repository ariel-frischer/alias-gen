import os
from pathlib import Path
from typing import Set, Union

from logger import debug


def find_file(file_path: Union[str, Path]) -> Path:
    path = Path(file_path)
    if path.exists() and os.path.isfile(path):
        return path.absolute()

    home_dir = Path.home()
    home_file_path = home_dir / file_path
    if home_file_path.exists() and os.path.isfile(home_file_path):
        return home_file_path.absolute()

    return home_dir.absolute()


def write_commands_to_file(commands: Set[str], filename: str):
    with open(filename, "w") as f:
        for command in sorted(commands):
            f.write(command + "\n")


def get_file_contents(file_path: Path) -> str:
    file_path = find_file(file_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "r") as f:
            file_contents = f.read()
        return file_contents
    else:
        debug(f"There was an issue reading file contents of path: {file_path}.")
        pass
        # raise argparse.ArgumentTypeError(f"{file_path} is not a valid file.")
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
