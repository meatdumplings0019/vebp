from colorama import Fore, Style


def print_python(version: str) -> None:
    print(f"Python版本: {Fore.CYAN}{version}{Style.RESET_ALL}")
    print()