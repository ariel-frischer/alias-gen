import re
import sys


def read_version(filename):
    with open(filename, "r") as f:
        content = f.read()
        match = re.search(r'version\s*=\s*"(\d+\.\d+\.\d+)"', content)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Version not found in {filename}")


def write_version(filename, version):
    with open(filename, "r") as f:
        content = f.read()

    with open(filename, "w") as f:
        content = re.sub(r'version\s*=\s*"\d+\.\d+\.\d+"', f'version="{version}"', content)
        f.write(content)


def bump_version(version, bump_type):
    version_parts = version.split(".")
    if bump_type == "minor":
        version_parts[1] = str(int(version_parts[1]) + 1)
        version_parts[2] = "0"
    elif bump_type == "major":
        version_parts[0] = str(int(version_parts[0]) + 1)
        version_parts[1] = "0"
        version_parts[2] = "0"
    else:
        raise ValueError("Invalid bump type. Use 'minor' or 'major'")

    return ".".join(version_parts)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python bump_version.py <bump_type> <file1> <file2> ...")
        sys.exit(1)

    bump_type = sys.argv[1]
    files = sys.argv[2:]

    for filename in files:
        version = read_version(filename)
        new_version = bump_version(version, bump_type)
        write_version(filename, new_version)

    print(f"Version bumped {bump_type}: {version} -> {new_version}")
