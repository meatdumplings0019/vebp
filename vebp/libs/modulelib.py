import importlib.util
import sys
from pathlib import Path
from typing import Union


class ModuleLoader:
    def __init__(self, package_path: Union[Path, str], package_name: str, main_module_name: str) -> None:
        self.package_path = package_path
        self.package_name = package_name
        self.main_module_name = main_module_name

        self.module = None

    def __enter__(self):
        spec = importlib.util.spec_from_loader(
            self.package_name,
            loader=None,
            origin=str(self.package_path),
            is_package=True
        )
        if spec is None:
            raise ImportError(f"无法创建包规范: {self.package_name}")

        # 创建包模块
        package_module = importlib.util.module_from_spec(spec)
        sys.modules[self.package_name] = package_module

        # 设置包路径
        package_module.__path__ = [str(self.package_path)]
        package_module.__package__ = self.package_name

        # 3. 加载主模块
        entry_file = self.package_path / self.main_module_name
        if not entry_file.exists():
            # 清理包模块
            del sys.modules[self.package_name]
            raise FileNotFoundError(f"入口文件 {self.main_module_name} 不存在")

        # 创建主模块规范
        main_module_name = f"{self.package_name}.main"
        spec = importlib.util.spec_from_file_location(
            main_module_name,
            str(entry_file),
            submodule_search_locations=[str(self.package_path)],
        )
        if spec is None:
            # 清理包模块
            del sys.modules[self.package_name]
            raise ImportError(f"无法创建模块规范: {entry_file}")

        main_module = importlib.util.module_from_spec(spec)
        sys.modules[main_module_name] = main_module

        try:
            # 设置主模块的包信息
            main_module.__package__ = self.package_name
            main_module.__path__ = [str(self.package_path)]

            # 执行主模块
            spec.loader.exec_module(main_module)
        except Exception as e:
            # 清理
            del sys.modules[main_module_name]
            del sys.modules[self.package_name]
            raise RuntimeError(f"主模块执行失败: {str(e)}")

        return main_module

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False