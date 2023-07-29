from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="alias-gen",
    version="0.3",
    author="Ariel Frischer",
    author_email="arielfrischer@gmail.com",
    description="Generate bash, zsh, or fish shell aliases automatically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ariel-frischer/alias-gen",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "aliaser = alias_gen.aliaser:main",
        ],
    },
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
