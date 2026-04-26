from pathlib import Path


pycharm_root = Path(r"C:\Users\chris\Documents\revamped projects\complement system tower defence 4")
suffixes = {".py", ".md", ".csv", ".html", ".xlsx", ".db", ".txt"}
exclude_files = {"__init__.py"}
exclude_dirs = {"__pycache__", ".pytest_cache", ".git", ".idea"}
exclude_dirs |= {"# other", "# matthew sql test"}


def is_file(path: Path) -> bool:
    """Checks if a path refers to a valid file."""
    return path.suffix in suffixes and path.name not in exclude_files

def is_dir(path: Path) -> bool:
    """Checks if a path refers to a valid directory."""
    return path.is_dir() and path.name not in exclude_dirs


def build_file_tree(dir_path: Path, depth=0, width=3, pre="", out="") -> str:
    """Recursively build the file structure from the given path."""
    paths = sorted(dir_path.glob("*"), key=lambda x: x.is_file())
    paths = [path for path in paths if is_file(path) or is_dir(path)]
    for ind, path in enumerate(paths, start=1):
        text = f"{pre}{'└' if ind == len(paths) else '├'}{'─' * width} {path.name}"
        if is_file(path):
            out += text + "\n"
        elif is_dir(path):
            out += text + "/\n"
            if ind == len(paths):
                out += build_file_tree(path, depth + 1, width, pre + " " * (width + 2))
            else:
                out += build_file_tree(path, depth + 1, width, pre + f"│{' ' * (width + 1)}")
    return (f"{dir_path.name}/\n" if depth == 0 else "") + out



if __name__ == "__main__":
    print(build_file_tree(pycharm_root))
