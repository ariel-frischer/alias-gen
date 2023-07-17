# ALIAS-GEN

Shell aliases are shortcuts or abbreviations for commands that are used in a Unix/Linux shell. They can save you time if you have very long or complex commands that you frequently use. ALIAS-GEN is a script that will create bash/zsh/fish shell aliases automatically to simplify your command-line tasks.

This script will create bash/zsh/fish shell aliases automatically. You can generate a new alias file by following the prompts, or use the `--stdout` option to print results directly in your terminal.

Two types of aliases are suggested, the default algorithm matches all characters incrementally for each command, while the `--use_min_alias`algorithm aims to minimize the total length of characters per command. 
Additionally, `--use_min_alias` does not necessarily match all characters in the command. 

The freq (frequency) column shows how often each command was used. For now, this script only generates aliases for the first word in a command. 
NOTE: Two character commands or less are not processed.

By default, fish shell generates abbr (abbreviations) rather than aliases.

## Requirements

- Python 3.6 or higher.
- No dependences required for installation.

## Getting Started

Clone this repo:

```
git clone <https://this-repo-url>
```

CD into the python source directory:

```
cd src/alias_gen
```

## Running the script

Full Help Menu:

```
python aliaser.py -h
```

Example usage to generate the top 40 aliases:

```
python aliaser.py -n 40
```

With stdout and min_alias:

```
python aliaser.py --stdout --use_min_alias
```

The `-s` argument specifies the shell type. In this example, `fish` shell is used.

```
python aliaser.py -s fish
```

The `-f` argument allows you to specify a custom history file path.

```
python aliaser.py -s zsh -f ~/.custom_zsh_history
```

## How does it work?

The `alias` column is generated by first sorting the most common commands found
in the history file, then aliases are generated for commands more than two
characters. These aliases just try to match character per character the given
command and will continue with more characters if there is a previous common
alias.

The `min_alias` column tries to minimize the total length of chars disregarding
the rule of matching the command character per character. It is generated using
the first char of the command always, followed by easy to reach keyboard characters
defined as QUERTY layout middle row, top row, then bottom row.

## Misc

I recommend using this script along with other shell plugins that help you remember
your alias or abbreviation. One example for fish shell is [fish-abbreviation-tips](https://github.com/gazorby/fish-abbreviation-tips).

## Buy me a coffee

If you found this project helpful, consider buying me a coffee to show your support. Every bit helps to continue maintaining and improving this project.

<a href="https://www.buymeacoffee.com/arielfrischer" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>


