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
        self._venv = ".venvs"
        self._script_path = None
        self._project_dir = None

        FolderStream(self.base_output_dir).create()

    @property
    def name(self) -> str:
        """获取项目名称"""
        return self._name

    @property
    def project_dir(self) -> Path:
        """获取项目目录"""
        return self._project_dir

    @property
    def venv(self) -> str:
        """获取虚拟环境路径"""
        return self._venv

    @venv.setter
    def venv(self, value: str) -> None:
        """设置虚拟环境路径"""
        self._venv = value

    @property
    def script_path(self) -> Path:
        """获取脚本路径"""
        return self._script_path

    @property
    def base_output_dir(self) -> Path:
        return Path.cwd() / build_name

    def set_script(self, script_path: str) -> "BaseBuilder":
        """
        设置脚本路径

        :param script_path: 脚本路径
        :return: 自身实例
        """
        if script_path:
            self._script_path = self._base_path / Path(script_path)
        return self

    def _validate(self) -> None:
        """验证构建器配置"""
        if not self.name:
            raise ValueError("项目名称是必需的")

    def build(self) -> None:
        """执行构建过程（由子类实现）"""
        pass