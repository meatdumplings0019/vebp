from colorama import Fore, Style


def print_color(color,
            *values,
            sep: str | None = " ",
            end: str | None = "\n",
            file = None,
            flush = False):
    print(f"{getattr(Fore, color, Fore.WHITE)}", end="")
    print(*values, sep=sep, end=end, file=file, flush=flush)
    print(f"{Style.RESET_ALL}", end="")

def print_red(
            *values,
            sep: str | None = " ",
            end: str | None = "\n",
            file = None,
            flush = False):
    print_color("RED", *values, sep=sep, end=end, file=file, flush=flush)