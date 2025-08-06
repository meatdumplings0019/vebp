import subprocess
from typing import Optional

from vebp.libs.system import SystemConsole


def is_python() -> tuple[bool, Optional[str], Optional[str]]:
    def run():
        cmd, version = SystemConsole.run_python(["--version"])
        return True, version.split(" ")[-1].strip(), cmd
    try:
        return run()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False, None, None