import pytest
from alias_gen.aliaser import (extract_commands, generate_alias,
                               generate_easy_alias, get_all_system_commands,
                               get_command_frequencies, print_results,
                               write_results)


@pytest.fixture
def mock_tui(mocker):
    return mocker.patch('alias_gen.tui.AliasGeneratorTUI')


def test_generate_alias():
    used_aliases = {"a", "ab", "abc"}
    used_easy_aliases = {"a", "b"}
    cmd = "abcd"
    alias, minimal_alias = generate_alias(cmd, used_aliases, used_easy_aliases)
    assert alias == "abcd"
    assert minimal_alias == "ab"


def test_generate_easy_alias():
    used_easy_aliases = {"a", "ab", "ac"}
    cmd = "abcd"
    minimal_alias = generate_easy_alias(cmd, used_easy_aliases)
    assert minimal_alias == "aa"


def test_get_command_frequencies():
    commands = ["ls", "ls", "pwd", "ls"]
    frequencies = get_command_frequencies(commands)
    assert frequencies == {"ls": 3, "pwd": 1}


def test_print_results(capsys):
    results = [("ls", 10, "lsalias", "lsa")]
    shell = "bash"
    use_alias = True
    print_results(results, shell, use_alias)
    captured = capsys.readouterr()
    assert captured.out == 'alias lsalias="ls"\n'


def test_write_results(tmp_path):
    results = [("ls", 10, "lsalias", "lsa")]
    shell = "bash"
    use_alias = True
    file_path = tmp_path / "output.txt"
    with open(file_path, "w") as f:
        write_results(f, results, shell, use_alias)
    content = file_path.read_text()
    assert content == 'alias lsalias="ls"\n'


def test_extract_commands():
    content = "- cmd: cat test.txt -v -h\n- cmd: pwd\n- cmd: git status"
    shell = "fish"
    commands = extract_commands(content, shell)
    assert commands == ["cat", "pwd", "git"]


def test_get_all_system_commands():
    commands_txt = "ls\tinfo\npwd\tinfo\ngit\n\n  \n"
    commands = get_all_system_commands(commands_txt)
    assert commands == {"ls", "pwd", "git"}
