import importlib.util
import sys
from pathlib import Path
from typing import Union, Optional, Dict, Callable

from vebp.libs.function import FunctionInjection


class ModuleLoader:
    def __init__(self, package_path: Union[Path, str], package_name: str, main_module_name: str, func_replacements: Optional[Dict[str, Callable]] = None, func_name: Optional[str] = None) -> None:
        self.package_path = package_path
        self.package_name = package_name
        self.main_module_name = main_module_name
        self.func_replacements = func_replacements or {}
        self.func_name = func_name or "func"

        self.module = None
        self.func_module = None

    def __enter__(self):
        # 创建包规范
        spec = importlib.util.spec_from_loader(
            self.package_name,
            loader=None,
            origin=str(self.package_path),
            is_package=True
        )
        if spec is None:
            raise ImportError(f"无法创建包规范: {self.package_name}")

        package_module = importlib.util.module_from_spec(spec)
        sys.modules[self.package_name] = package_module

        package_module.__path__ = [str(self.package_path)]
        package_module.__package__ = self.package_name

        with FunctionInjection(self.package_path, self.package_name, self.func_name, self.func_replacements) as module:
            self.func_module = module

        entry_file = self.package_path / self.main_module_name
        if not entry_file.exists():
            func_module_name = f"{self.package_name}.func"
            if func_module_name in sys.modules:
                del sys.modules[func_module_name]
            del sys.modules[self.package_name]
            raise FileNotFoundError(f"入口文件 {self.main_module_name} 不存在")

        main_module_name = f"{self.package_name}.main"
        spec = importlib.util.spec_from_file_location(
            main_module_name,
            str(entry_file),
            submodule_search_locations=[str(self.package_path)],
        )
        if spec is None:
            func_module_name = f"{self.package_name}.func"
            if func_module_name in sys.modules:
                del sys.modules[func_module_name]
            del sys.modules[self.package_name]
            raise ImportError(f"无法创建模块规范: {entry_file}")

        main_module = importlib.util.module_from_spec(spec)
        sys.modules[main_module_name] = main_module

        try:
            main_module.__package__ = self.package_name

            spec.loader.exec_module(main_module)
        except Exception as e:
            del sys.modules[main_module_name]
            func_module_name = f"{self.package_name}.func"
            if func_module_name in sys.modules:
                del sys.modules[func_module_name]
            del sys.modules[self.package_name]
            raise RuntimeError(f"主模块执行失败: {str(e)}")

        return main_module

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False