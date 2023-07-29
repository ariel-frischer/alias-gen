DEFAULT_SHELL = "zsh"
SUPPORTED_SHELLS = ["bash", "zsh", "fish"]
INVALID_CMD_CHAR_REGEX = r"^[^a-zA-Z]+$"

SUPPORTED_FILE_ENCODINGS = [
    None,
    "utf-8",
    "Windows-1251",
    "Windows-1252",
    "GB2312",
    "Shift JIS",
    "GBK",
    "EUC-KR",
    "ISO-8859-9",
    "Windows-1254",
    "EUC-JP",
    "Big5",
    "unknown-8bit",
]

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
