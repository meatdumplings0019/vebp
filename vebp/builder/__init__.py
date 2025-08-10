from pathlib import Path
from typing import Optional

from vebp.config import build_name
from vebp.libs.file import FolderStream
from vebp.libs.path import MPath


class BaseBuilder:
    def __init__(self, app, name: Optional[str], base_path: str = "."):
        self.app = app
        self._name = name
        self._base_path = MPath.to_path(base_path)
        self._venv = ".venv"
        self._script_path = None
        self._project_dir = None

        FolderStream(self.base_output_dir).create()

    @property
    def name(self) -> str:
        return self._name

    @property
    def project_dir(self) -> Path:
        return self._project_dir

    @property
    def venv(self) -> str:
        return self._venv

    @venv.setter
    def venv(self, value: str) -> None:
        self._venv = value

    @property
    def script_path(self) -> Path:
        return self._script_path

    @property
    def base_output_dir(self) -> Path:
        return Path.cwd() / build_name

    def set_script(self, script_path: str) -> "BaseBuilder":
        if script_path:
            self._script_path = self._base_path / Path(script_path)
        return self

    def _validate(self) -> None:
        if not self.name:
            raise ValueError("项目名称是必需的")

    def build(self) -> None:
        pass