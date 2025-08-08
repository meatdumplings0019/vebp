import importlib.util
import sys
from pathlib import Path
from typing import Union, Optional, Dict, Callable


class ModuleLoader:
    def __init__(
            self,
            package_path: Union[Path, str],
            package_name: str,
            main_module_name: str,
            func_replacements: Optional[Dict[str, Callable]] = None
    ) -> None:
        self.package_path = package_path
        self.package_name = package_name
        self.main_module_name = main_module_name
        self.func_replacements = func_replacements or {}

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

        # 创建包模块
        package_module = importlib.util.module_from_spec(spec)
        sys.modules[self.package_name] = package_module

        # 设置包路径
        package_module.__path__ = [str(self.package_path)]
        package_module.__package__ = self.package_name

        # 1. 加载func.py模块（如果存在）
        func_file = self.package_path / "func.py"
        if func_file.exists():
            # 创建func模块规范
            func_module_name = f"{self.package_name}.func"
            func_spec = importlib.util.spec_from_file_location(
                func_module_name,
                str(func_file),
                submodule_search_locations=[str(self.package_path)],
            )
            if func_spec is None:
                # 清理包模块
                del sys.modules[self.package_name]
                raise ImportError(f"无法创建func模块规范: {func_file}")

            # 创建func模块
            self.func_module = importlib.util.module_from_spec(func_spec)
            sys.modules[func_module_name] = self.func_module

            # 设置func模块的包信息
            self.func_module.__package__ = self.package_name

            try:
                # 执行func模块
                func_spec.loader.exec_module(self.func_module)

                # 替换func模块中的函数
                for func_name, replacement in self.func_replacements.items():
                    if hasattr(self.func_module, func_name):
                        setattr(self.func_module, func_name, replacement)
            except Exception as e:
                # 清理
                del sys.modules[func_module_name]
                del sys.modules[self.package_name]
                raise RuntimeError(f"func模块执行失败: {str(e)}")

        # 2. 加载主模块
        entry_file = self.package_path / self.main_module_name
        if not entry_file.exists():
            # 清理包模块和func模块
            func_module_name = f"{self.package_name}.func"
            if func_module_name in sys.modules:
                del sys.modules[func_module_name]
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
            # 清理包模块和func模块
            func_module_name = f"{self.package_name}.func"
            if func_module_name in sys.modules:
                del sys.modules[func_module_name]
            del sys.modules[self.package_name]
            raise ImportError(f"无法创建模块规范: {entry_file}")

        main_module = importlib.util.module_from_spec(spec)
        sys.modules[main_module_name] = main_module

        try:
            # 设置主模块的包信息
            main_module.__package__ = self.package_name

            # 执行主模块
            spec.loader.exec_module(main_module)
        except Exception as e:
            # 清理
            del sys.modules[main_module_name]
            func_module_name = f"{self.package_name}.func"
            if func_module_name in sys.modules:
                del sys.modules[func_module_name]
            del sys.modules[self.package_name]
            raise RuntimeError(f"主模块执行失败: {str(e)}")

        return main_module

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 不再清理func模块，插件运行期间需要保持加载状态
        return False