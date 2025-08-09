from vebp.libs.venvs import venv_path


def pip_command(venv: str = ".venv") -> list[str]:
    python = venv_path(venv)

    return [f"{python}", "-m", "pip"]