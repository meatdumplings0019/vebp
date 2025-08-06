import sys

from vebp.libs.system import SystemConsole


def wait_for_any_key():
    # Windows系统
    if SystemConsole.windows():
        import msvcrt
        print("请按任意键退出...")
        msvcrt.getch()

    print()
    sys.exit()