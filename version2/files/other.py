def format_number(x: int, suffixes=("", "K", "M", "B", "T", "Q")) -> str:
    x = str(x)
    comma = "," if (len(x) - 1) % 3 == 0 and len(x) > 1 else ""
    y = x[0] + comma + x[1:]
    for i in range(len(suffixes)):
        if len(x) <= (i + 1) * 3 + 1:
            return y[0:len(y) - i * 3] + suffixes[i]
