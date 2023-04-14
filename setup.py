import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alias-gen",  # Replace with your package name
    version="0.1",  # Replace with your package version
    author="Ariel Frischer",  # Replace with your name
    author_email="arielfrischer@gmail.com",  # Replace with your email
    description="Generate bash, zsh, or fish shell aliases automatically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ariel-frischer/alias-gen",  # Replace with your package URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "alias",
        "bash",
        "zsh",
        "fish",
        "shell",
        "cli",
        "command-line",
        "command",
        "completion",
        "abbr",
        "generate",
        "terminal",
    ],
)
