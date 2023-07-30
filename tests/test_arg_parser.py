from pathlib import Path

import pytest

from alias_gen.file_utils import (find_file, get_encoding, get_file_contents,
                                  get_history_file_path)


def test_find_file(tmp_path):
    # Case 1: File exists at the given path
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test content")
    assert find_file(file_path) == file_path.absolute()

    # Case 2: File doesn't exist at given path, but exists in home directory
    home_dir = Path.home()
    home_file_path = home_dir / "home_test_file.txt"
    home_file_path.write_text("Home directory test content")
    assert find_file("home_test_file.txt") == home_file_path.absolute()

    # Clean up home directory file
    home_file_path.unlink()

    # Case 3: File doesn't exist at given path or in home directory
    non_existent_file_path = "non_existent_file.txt"
    assert find_file(non_existent_file_path) == home_dir.absolute()

def test_get_encoding():
    # utf-8 is technically still ascii, so encoding with utf-8 will result in
    # chardet returning ascii
    test_file_path = "temp_test_file.txt"
    test_encoding = "ascii"
    content = "This is a test file with a known encoding."

    with open(test_file_path, "w", encoding=test_encoding) as f:
        f.write(content)

    detected_encoding = get_encoding(test_file_path)

    assert detected_encoding == test_encoding

    # Optionally, remove the temporary test file
    Path(test_file_path).unlink()


def test_get_file_contents():
    current_dir = Path.cwd()
    test_file = current_dir / "test_file.txt"
    with open(test_file, "w") as f:
        f.write("test")
    assert get_file_contents("test_file.txt") == "test"

    non_existent_file = "non_existent_file.txt"
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
