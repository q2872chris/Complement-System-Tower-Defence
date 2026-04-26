from pathlib import Path


def safe_sum(iterable: iter) -> iter:
    """Can sum any iterable with items that have compatible __add__ methods,
     for example a list of strings."""
    return sum(iterable[1:], iterable[0])


def get_root(start: Path, flag="main.py") -> Path:
    path = start.resolve()
    while path != path.parent:
        if (path / flag).exists():
            return path
        path = path.parent
    raise FileNotFoundError(f"Could not find {flag} in any parent directories.")


self_path = Path(__file__).absolute()
root = get_root(self_path)


class line_count_container:
    def __init__(self, path: (Path | None), lines: list[str] = None, files=1):
        self.files = files
        self.lines = lines
        self.name = "" if path is None else path.relative_to(root)
        self.count = (0, 0, 0, 0.0, 0.0, 0.0)
        self.count_no_blank_lines = (0, 0, 0, 0.0, 0.0, 0.0)
        self.count_no_comments = (0, 0, 0, 0.0, 0.0, 0.0)
        self.count_no_imports = (0, 0, 0, 0.0, 0.0, 0.0)
        if lines is None:
            self.get_module_lines(path)
        self.count_module_lines(self.lines)

    @staticmethod
    def file_stats(lines: list[str]) -> tuple[int, int, int, float, float, float]:
        """Returns the number of lines and the number of characters."""
        tokens = [[len(token) for token in line.split(' ')] for line in lines if line]
        return len(lines), sum(len(line.replace(' ', '')) for line in lines), \
            sum(line.count(' ') + 1 for line in lines if line), \
            round(sum(len(line) for line in lines) / (len(lines) + 1), 1), \
            round(sum(len(i) for i in tokens) / (len(lines) + 1), 1), \
            round(sum(a := sum(tokens, [])) / (len(a) + 1), 1)

    def get_module_lines(self, path: Path):
        with open(path) as reader:
            lines = [i.strip() for i in reader.readlines()]
            while len(lines) > 0 and lines[-1] == '':
                lines.pop(-1)
            self.lines = lines

    def count_module_lines(self, lines: list[str]):
        no_white_space = [i for i in lines if i != '']
        no_comments = [i for i in no_white_space if i[0] != '#']
        no_imports = [i for i in no_comments if "import" not in i]
        self.count = self.file_stats(lines)
        self.count_no_blank_lines = self.file_stats(no_white_space)
        self.count_no_comments = self.file_stats(no_comments)
        self.count_no_imports = self.file_stats(no_imports)

    def print(self, print_name=True) -> str:
        messages = ["{0}: {%s}" + " " * 37, "{0} (excluding blank lines): {%s}" + " " * 13,
                    "{0} (excluding blank lines and comments): {%s}",
                    "{0} (excluding the above and imports): {%s}   "]
        extra = "   (Characters: {%s})   (Tokens: {%s})   (Average line length: {%s})" + \
                "   (Average # of tokens per line: {%s})   (Average token length: {%s})"
        messages = [m + ("   " if self.files == 1 else "") + extra for m in messages]
        n = messages[0].count("%s")
        messages = [m % tuple(range(i * n + 1, (i + 1) * n + 1)) for i, m in enumerate(messages)]
        sep = "\n\t" if print_name else "\n"
        message = f"{self.name}:" if print_name else ""
        message += ("\n\t" if print_name else "") + sep.join(messages)
        message += f"{sep}Total python files: {self.files}" if self.files > 1 else ""
        return message.format("Lines" if self.files == 1 else "Total lines",
                              *self.count, *self.count_no_blank_lines,
                              *self.count_no_comments, *self.count_no_imports)

    def __str__(self) -> str:
        return self.print()

    def __add__(self, other) -> "line_count_container":
        self.name = f"{self.name} & {other.name}"
        self.lines += other.lines
        self.count_module_lines(self.lines)
        self.files += 1
        return self

    @staticmethod
    def sum_containers(*args: "line_count_container") -> "line_count_container":
        lines = safe_sum([i.lines for i in args])
        return line_count_container(None, lines, len(args))


def count_total_lines(sorting_mode="None", reverse=False, exclude_self=False,
                      exclude_init=False, exclude_list=()):
    all_files = [path for path in root.rglob("*") if
                 not any(i in str(path) for i in exclude_list) and
                 path.suffix in ("", ".py", ".png", ".db") and path.is_file() and
                 "__pycache__" not in str(path) and ".idea" not in str(path)]
    full_counts = [line_count_container(path) for path in all_files if
                   path.suffix in ("", ".py")]
    counts = [obj for obj in full_counts if obj.name.suffix == ".py" and
              (obj.name != self_path.relative_to(root) or not exclude_self) and
              ("__init__.py" not in str(obj.name) or not exclude_init)]
    if sorting_mode in ("count", "count_no_blank_lines",
                        "count_no_comments", "count_no_imports"):
        counts.sort(key=lambda x: getattr(x, sorting_mode), reverse=reverse)
    print("Module line counts:")
    print(*counts, sep="\n")
    print(line_count_container.sum_containers(*counts).print(print_name=False))
    print("Character stats don't include spaces/tabs/etc, they do include in-line comments.")
    message = "Line length stats%sinclude %s."
    print(message % (" don't " if exclude_self else " ", "this file"))
    print(message % (" don't " if exclude_init else " ", "__init__.py files"))
    print("\nExtra info (any file with text):")
    print(line_count_container.sum_containers(*full_counts).print(print_name=False))
    print(f"Total of all types of file: {len(all_files)}")
    print("Author of this script: Christopher Wiseman")


if __name__ == "__main__":
    count_total_lines(sorting_mode="count_no_imports", exclude_self=True,
                      exclude_init=True, exclude_list=("#", ))

