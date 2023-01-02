# ALIAS-GEN

This script will create bash/zsh/fish shell aliases automatically. You can generate a new alias file by following the prompts, or use --stdout to print results directly in your terminal.

Two types of aliases are suggested, the default alias matches all characters in the command while min_alias aims to minimize the length of characters. Additionally, min_alias does not necessarily match all characters in the command. The freq (frequency) column shows how often this command was used. For now, this script only generates aliases for the first word in a command. NOTE: Two character commands or less are not processed.

By default, fish shell generates abbr (abbreviations) rather than aliases.

## Getting Started

Clone this repo:

```
git clone <https://this-repo-url>
```

CD into the repo directory:

```
cd alias-gen
```

## Running the script

Full Help Menu:

```
python aliaser.py -h
```

Example usage with top 40 aliases:

```
python aliaser.py -n 40
```

With stdout and min_alias:

```
python aliaser.py --stdout --use_min_alias
```

Generate for fish shell:

```
python aliaser.py -s fish
```

Generate for zsh with custom history file path:

```
python aliaser.py -s zsh -f ./.custom_zsh_history
```

## Misc

I recommend using this script along with other shell plugins that help you remember
your alias or abbreviation. One example for fish shell is [fish-abbreviation-tips](https://github.com/gazorby/fish-abbreviation-tips)

## Buy me a coffee

If you found this project helpful, consider buying me a coffee to show your support. Every bit helps to continue maintaining and improving this project.

<a href="https://www.buymeacoffee.com/arielfrischer" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## TODO
- [ ] Fix comands that start with ./script.sh cannot have alias of . or /
- [ ] Add arg to allow alias for fish over abbr.
- [ ] Put more debug statements in stategic places

- [x] Move this script into its own repo
- [ ] Package everything with poetry
- [x] Add an MIT license
Create an executable! - pipeline that builds it would be nice.
Publish to public gitlab
Publish to public github
Write an article about this and how ChatGPT helped write boilerplate.
Publish my own website with that article.
Post my article and repo to some subreddits

## Author

- **[Ariel Frischer Gitlab](https://gitlab.com/ariel-frischer)**
- **[Ariel Frischer Github](https://github.com/ariel-frischer)**
