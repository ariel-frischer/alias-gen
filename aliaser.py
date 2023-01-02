"""
Module name: alias_gen
Author: Ariel Frischer
Date created: 2022-01-01
Description: Generate aliases for your shell.
"""

import argparse
import itertools
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple

from arg_parser import parse_args
from constants import SUPPORTED_SHELLS
from logger import debug, init_logger
from file_utils import get_file_contents, write_commands_to_file, get_history_file_path, find_file

ResType = List[Tuple[str, int, str, str]]

comment = """
TODO:
Fix comands that start with ./script.sh cannot have alias of . or /
Add arg to allow alias for fish over abbr.
Put more debug statements in stategic places

Move this script into its own repo
Let ChatGPT write scripts for this
Package everything with poetry
Add an MIT license
Push to my private gitlab
Create an executable! - pipeline that builds it would be nice.
Create some buy me coffee or donate link stuff on my github / gitlab
Publish to public gitlab
Publish to public github
Write an article about this and how ChatGPT helped write boilerplate.
Publish my own website with that article.
"""

easy_chars = "asdfghjklqwertyuiopzxcvbnm"  # easy to reach on keyboard
# Not using this right now but holds potential to pull more types
cmd_gets_cmds = "printf '%s\n' ${PATH//:/\/* } | xargs -n 1 basename"


def main(args: argparse.Namespace):

    shell = args.s
    hist_path = args.f
    max_suggestions = args.n

    sorted_commands, used_aliases = get_all_commands(hist_path, shell)

    results = gen_aliases(max_suggestions, sorted_commands, used_aliases)

    if args.stdout:
        print_results(results, shell, not args.use_min_alias)
    else:
        show_alias_chart(results)
        write_to_file_prompt(results, shell, args.use_min_alias)


def print_results(results: ResType, shell: str, use_alias: bool):
    for cmd, freq, alias, minimal_alias in results:
        if shell == "fish":
            print(f"abbr {cmd} '{alias if use_alias else minimal_alias}'")
        else:
            print(f'alias {alias if use_alias else minimal_alias}="{cmd}"')


def write_results(f, results: ResType, shell: str, use_alias: bool):
    for cmd, freq, alias, minimal_alias in results:
        if shell == "fish":
            f.write(f"abbr {cmd} '{alias if use_alias else minimal_alias}'\n")
        else:
            f.write(f'alias {alias if use_alias else minimal_alias}="{cmd}"\n')


def use_alias_prompt(use_min_alias: bool):
    if use_min_alias:
        return False

    prompt = "Do you want to use the alias column? [Y/n] "
    use_alias_res = input(prompt)
    return use_alias_res.lower() == "y" or use_alias_res == ""


#
def write_to_file_prompt(results: ResType, shell: str, use_min_alias: bool) -> None:
    write_to_file = input("Do you want to write output to a file? [Y/n] ")

    if write_to_file.lower() == "y" or write_to_file == "":
        use_alias = use_alias_prompt(use_min_alias)
        msg = "alias" if use_alias else "min_alias"
        print(f"Using the {msg} list.")

        file_name = input("Enter a file name: ")
        if not os.path.exists(file_name):
            open(file_name, "w").close()
        with open(file_name, "w") as f:
            write_results(f, results, shell, use_alias)

        print(f"File {file_name} written successfully!")
    else:
        print("No file written")


def get_all_commands(hist_path: Path, shell: str):
    history_commands = get_history_commands(shell, hist_path)
    debug(f"Found {len(history_commands)} history commands")
    debug(f"History commands: {history_commands[:10]}")

    frequency = get_command_frequencies(history_commands)
    sorted_commands = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    debug(f"Sorted History commands: {sorted_commands[:10]}")

    sys_commands = get_system_commands(shell)
    debug(f"Found {len(sys_commands)} system commands")

    used_aliases = set([tup[0] for tup in sorted_commands]) | sys_commands
    sorted_commands = sorted_commands + sorted([(cmd, 0) for cmd in sys_commands])
    return sorted_commands, used_aliases


def get_history_commands(shell: str, hist_path: Path) -> List[str]:
    history_commands = []
    history_path = (
        hist_path if os.path.isfile(hist_path) else get_history_file_path(shell)
    )
    if history_path:
        history = get_file_contents(history_path)
        history_commands = extract_commands(history, shell)
    return history_commands


def gen_aliases(
    max_suggestions: int, sorted_commands: List[Tuple[str, int]], used_aliases: Set[str]
):
    used_easy_aliases = used_aliases.copy()
    results = []
    for cmd, freq in sorted_commands[:max_suggestions]:
        cmd_words = cmd.split()
        alias, minimal_alias = generate_alias(
            cmd_words[0], used_aliases, used_easy_aliases
        )
        used_aliases.add(alias)
        used_easy_aliases.add(minimal_alias)
        results.append((cmd, freq, alias, minimal_alias))
    return results


def show_alias_chart(results: List[Tuple[str, int, str, str]]):
    th = ("cmd", "freq", "alias", "min_alias")
    print(f"{th[0]:<20}{th[1]:<10}{th[2]:<10}{th[3]:<10}\n")

    for cmd, freq, alias, minimal_alias in results:
        f_cmd = cmd[:15] if len(cmd) <= 15 else (cmd[:15] + "...")
        print(f"{f_cmd:<20}{freq:<10}{alias:<10}{minimal_alias:<10}")


def extract_commands(file_contents: str, shell: str) -> List[str]:
    commands = []
    regex = r"- cmd: (.*)" if shell == "fish" else r"(.*)$"
    for line in file_contents.split("\n"):
        match = re.search(regex, line)
        if match:
            first_word = match.group(1).split(" ", 1)[0]
            if len(first_word) > 2:
                commands.append(first_word)
    return commands


def get_command_frequencies(commands: List[str]) -> Dict[str, int]:
    frequency: Dict[str, int] = {}
    for cmd in commands:
        if cmd:
            frequency[cmd] = frequency.get(cmd, 0) + 1
    return frequency


def get_all_system_commands(commands_txt: str) -> Set[str]:
    commands = commands_txt.split("\n")
    commands = [cmd.split("\t")[0] for cmd in commands]
    return set(commands)


invalid_cmd_char_regex = r"^[^a-zA-Z]+$"
invalid_commands = [
    "*",
    "!",
    ".",
    ":",
    "[",
    "]",
    "]]",
    "[[",
    "{",
    "}",
    "elif",
    "else",
    "bin",
    "if",
    "in",
    "let",
]


def get_system_commands(shell: str) -> Set[str]:
    if shell not in SUPPORTED_SHELLS:
        raise ValueError(
            f"{shell} is not a supported shell. Supported shells: {SUPPORTED_SHELLS}"
        )

    compgen_command = "bash -c 'compgen -c' | sort | uniq"
    if shell == "bash":
        command = compgen_command
    elif shell == "zsh":
        command = compgen_command
        # command = "zsh -c 'compgen -c'"
    elif shell == "fish":
        command = compgen_command
        # command = "fish -c 'complete -C'"
    else:
        raise ValueError(f"Unsupported shell: {shell}")

    output = (
        subprocess.run(command, shell=True, capture_output=True).stdout.decode().strip()
    )
    commands = set(output.split("\n"))

    filtered_commands = [c for c in commands if c not in invalid_commands]
    filtered_commands = [c for c in commands if not re.match(invalid_cmd_char_regex, c)]
    commands = set(filtered_commands)
    debug(f"total sys commands: {len(commands)}")

    return commands


def generate_alias(cmd: str, used_aliases: Set[str], used_easy_aliases: Set[str]):
    alias = ""

    for c in cmd:
        if alias and alias not in used_aliases:
            break
        alias += c

    minimal_alias = generate_easy_alias(cmd, used_easy_aliases)

    return (alias, minimal_alias)


def generate_easy_alias(cmd: str, used_easy_aliases: Set[str]) -> str:
    alias = first_char = cmd[0]

    if first_char not in used_easy_aliases:
        return first_char

    count = 0
    while count < len(cmd):
        count += 1
        alias = cmd[0 : count + 1]
        if alias not in used_easy_aliases:
            return alias

        permutations = itertools.permutations(easy_chars, count)

        for permutation in permutations:
            alias = first_char + "".join(permutation)
            if alias not in used_easy_aliases:
                return alias

    return cmd


if __name__ == "__main__":
    args = parse_args()
    init_logger(args)
    debug(f"args: {args}")

    main(args)
