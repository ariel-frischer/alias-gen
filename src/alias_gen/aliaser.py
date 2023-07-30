"""
Module name: alias_gen
Author: Ariel Frischer
Date created: 2022-01-01
Description: Generate aliases for your shell.
"""

import itertools
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .arg_parser import parse_args
from .constants import INVALID_CMD_CHAR_REGEX, INVALID_COMMANDS
from .file_utils import get_file_contents, get_history_file_path
from .logger import debug, init_logger

ResType = List[Tuple[str, int, str, str]]

easy_chars = "asdfghjklqwertyuiopzxcvbnm"  # easy to reach on keyboard
# Not using this right now but holds potential to pull more types
cmd_gets_cmds = "printf '%s\n' ${PATH//:/\/* } | xargs -n 1 basename"


def main():
    args = parse_args()
    debug(f"args: {args}")

    shell, hist_path, max_suggestions = args.s, args.f, args.n

    if not args.stdout:
        print(f"Detected shell: {shell}")

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
            print(f"abbr {alias if use_alias else minimal_alias} '{cmd}'")
        else:
            print(f'alias {alias if use_alias else minimal_alias}="{cmd}"')


def write_results(f, results: ResType, shell: str, use_alias: bool):
    for cmd, freq, alias, minimal_alias in results:
        if shell == "fish":
            f.write(f"abbr {alias if use_alias else minimal_alias} '{cmd}'\n")
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

    bash_commands = get_bash_commands(shell)
    shell_commands = get_shell_commands(shell)
    sys_commands = bash_commands | shell_commands
    debug(f"Found {len(sys_commands)} system commands")

    used_aliases = set([tup[0] for tup in sorted_commands]) | sys_commands
    sorted_commands = sorted_commands + sorted([(cmd, 0) for cmd in sys_commands])
    return sorted_commands, used_aliases


def get_history_commands(shell: str, hist_path: Path) -> List[str]:
    history_commands = []
    history_path = hist_path if os.path.isfile(hist_path) else get_history_file_path(shell)

    if history_path:
        history = get_file_contents(history_path)
        history_commands = extract_commands(history, shell)
    return history_commands


def gen_aliases(max_suggestions: int, sorted_commands: List[Tuple[str, int]], used_aliases: Set[str]):
    used_easy_aliases = used_aliases.copy()
    results = []
    for cmd, freq in sorted_commands[:max_suggestions]:
        cmd_words = cmd.split()
        alias, minimal_alias = generate_alias(cmd_words[0], used_aliases, used_easy_aliases)
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
    if shell == "fish":
        regex = r"- cmd: (.*)"
    else:  # Assume zsh
        regex = r": \d+:\d+;(.*)"
    for line in file_contents.split("\n"):
        match = re.search(regex, line)
        if match:
            command = match.group(1).strip()
            if command:
                first_word = command.split(" ", 1)[0]
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
    commands = [c for c in commands if c.strip()]
    return set(commands)


def get_bash_commands(shell: str) -> Set[str]:
    compgen_command = "bash -c 'compgen -c'"
    command = compgen_command

    debug(f"Running bash command: {command}")
    output = subprocess.run(command, shell=True, capture_output=True).stdout.decode().strip()
    # debug(f"Output: {output}")
    commands = set(output.split("\n"))

    filtered_commands = [c for c in commands if c not in INVALID_COMMANDS and c]
    commands = set(filtered_commands)
    debug(f"total bash commands: {len(commands)}")

    return commands


def get_shell_commands(shell: str) -> Set[str]:
    command = ""
    if shell == "bash":
        return set()
    elif shell == "zsh":
        return set()
    elif shell == "fish":
        command = "fish -c 'complete -C \"\"'"
    else:
        debug(f"Unsupported shell: {shell}")

    debug(f"Running shell command: {command}")
    output = subprocess.run(command, shell=True, capture_output=True).stdout.decode().strip()

    if shell == "fish":
        # Strip out all lines that contain these patterns
        remove_rx = r"^.*(Abbreviation: .*$)|^.*(alias .*$)|^.*(directory$)"
        output = re.sub(remove_rx, "", output, flags=re.MULTILINE)
        rx = r"^([^ \t]+).*"
        output = re.sub(rx, r"\1", output, flags=re.MULTILINE)

    commands = set(output.split("\n"))

    filtered_commands = [c for c in commands if c not in INVALID_COMMANDS and c]
    commands = set(filtered_commands)

    debug(f"total shell commands: {len(commands)}")

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
    main()
