DEFAULT_SHELL = "zsh"
SUPPORTED_SHELLS = ["bash", "zsh", "fish"]
INVALID_CMD_CHAR_REGEX = r"^[^a-zA-Z]+$"

INVALID_COMMANDS = [
    " ",
    "\t",
    "*",
    "!",
    ".",
    ":",
    "_",
    "-",
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
