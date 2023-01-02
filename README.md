# ALIAS-GEN

This script will create bash/zsh/fish shell aliases automatically. You can generate a new alias file by following the prompts, or use --stdout to print results directly in your terminal.

Two types of aliases are suggested, the default alias matches all characters in the command while min_alias aims to minimize the length of characters. Additionally, min_alias does not necessarily match all characters in the command. The freq (frequency) column shows how often this command was used. For now, this script only generates aliases for the first word in a command. NOTE: Two character commands or less are not processed.

By default, fish shell generates abbr (abbreviations) rather than aliases.

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
your alias or abbreviation. One example for fish shell is https://github.com/gazorby/fish-abbreviation-tips

## Buy me a coffee

If you found this project helpful, consider buying me a coffee to show your support. Every bit helps to continue maintaining and improving this project.

buy me a coffee

## Author

- **[Ariel Frischer Gitlab](https://gitlab.com/ariel-frischer)**
- **[Ariel Frischer Github](https://github.com/ariel-frischer)**
