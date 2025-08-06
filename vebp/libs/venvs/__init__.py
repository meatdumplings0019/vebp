from pathlib import Path

from vebp.libs.system import SystemConsole


def venv_path(venv: str = ".venvs") -> Path:
    python = SystemConsole.python_venv(Path.cwd() / venv)

    if python.exists():
        return python

    return Path(SystemConsole.run_python(["-c", "import sys; print(sys.executable)"])[1])