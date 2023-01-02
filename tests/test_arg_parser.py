import pytest
from pathlib import Path

from alias_gen.file_utils import get_file_contents, get_history_file_path, find_file

non_existent_file = "non_existent_file_64787f59-181b-4ab6-b430-5c8c571b8fe4.txt"

def test_find_file():
    current_dir = Path.cwd()
    test_file = current_dir / "test_file.txt"
    # with open(test_file, "w") as f:
    #     f.write("test")
    assert find_file("test_file.txt") == test_file.absolute()

    home_dir = Path.home()
    # test_file = home_dir / "test_file.txt"
    # with open(test_file, "w") as f:
    #     f.write("test")
    # assert find_file("test_file.txt") == test_file.absolute()

    assert find_file(non_existent_file) == home_dir.absolute()

    test_file.unlink()


def test_get_file_contents():
    current_dir = Path.cwd()
    test_file = current_dir / "test_file.txt"
    with open(test_file, "w") as f:
        f.write("test")
    assert get_file_contents("test_file.txt") == "test"

    print(get_file_contents(non_existent_file))
    assert get_file_contents(non_existent_file) == ""

    test_file.unlink()


def test_get_history_file_path():
    home_dir = Path.home()
    expected_path = home_dir / ".local/share/fish/fish_history"
    assert get_history_file_path("fish") == expected_path

    expected_path = home_dir / ".bash_history"
    assert get_history_file_path("bash") == expected_path

    expected_path = home_dir / ".zsh_history"
    assert get_history_file_path("zsh") == expected_path

    assert get_history_file_path("csh") == home_dir
