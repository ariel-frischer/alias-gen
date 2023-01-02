import os
from pathlib import Path

from typing import Union


def find_file(file_path: Union[str, Path]) -> Path:
    path = Path(file_path)
    if path.exists() and os.path.isfile(path):
        return path.absolute()

    home_dir = Path.home()
    home_file_path = home_dir / file_path
    if home_file_path.exists() and os.path.isfile(home_file_path):
        return home_file_path.absolute()

    return home_dir.absolute()
