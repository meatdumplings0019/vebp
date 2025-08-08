import ast
import os
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Dict, Any, Optional, List, cast

from vebp.data.package import Package
from vebp.libs.file import FolderStream, FileStream
from vebp.libs.modulelib import ModuleLoader
from vebp.libs.path import MPath
from vebp.libs.zip import ZipContent
from vebp.plugin import Plugin

def plugin_get_assets_path(app, namespace):
    return app.plugin_manager.get_plugin(namespace).assets

class PluginManager:
    def __init__(self, app):
        """
        插件管理器初始化
        """
        # 插件存储字典: {namespace: PluginConfig 实例}
        self.app = app

        self.plugins: Dict[str, Plugin] = {}
        # 记录插件包名到路径的映射
        self.package_paths: Dict[str, str] = {}
        # 记录每个插件添加的依赖路径
        self.dependency_paths: Dict[str, List[str]] = {}

        self.function_registry: Dict[str, Callable] = {
            "get_assets_path": plugin_get_assets_path,
        }

    def load_all_plugin(self):
        """
        加载指定目录下的所有插件
        """
        f = FolderStream(self.app.plugins)

        for fs in f.walk().files:
            if fs.suffix == ".zip":
                self.load_plugin(fs.path)

        for ff in f.walk().folders:
            self.load_plugin(ff.path)

        p_lst = self.app.settings.config.get("plugins", [], "add")
        if p_lst:
            for p in p_lst:
                self.load_plugin(p)

        self.app.plugin_data.update_state()

    def load_plugin(self, path: str | Path):
        try:
            plugin = Path(str(path))

            if FileStream(plugin).suffix == ".zip":
                with ZipContent(plugin) as zipf:
                    self._load_single_plugin(zipf)

            if plugin.is_dir():
                self._load_single_plugin(plugin)

            self.app.plugin_data.update_state()

        except Exception as e:
            print(f"🔥 解析失败[{path}]: {str(e)}]")

    def install(self, path) -> bool:
        path = MPath.to_path(path)
        if not path.exists():
            raise FileNotFoundError(f"此文件不存在")

        des: Path = self.app.plugins

        out = des / path.name

        if path.is_dir(): des /= path.name

        if out.exists():
            shutil.rmtree(out, ignore_errors=True)

        result = FileStream.copy(path, des)

        try:
            if not result:
                raise
            self.load_plugin(des)
            return True
        except Exception as e:
            print(f"{e}")
            return False

    def uninstall(self, name) -> None:
        self.unload_plugin(name)
        src = self.app.plugins / name
        if not src.is_dir():
            name = f'{name}.zip'
            src = self.app.plugins / name

        FileStream.delete(src)

    def _add_dependencies_to_path(self, plugin_dir: Path, namespace: str):
        """将插件的依赖目录添加到系统路径"""
        dependencies_dir = plugin_dir / "dependencies"
        added_paths = []

        # 检查依赖目录是否存在
        if dependencies_dir.exists() and dependencies_dir.is_dir():
            print(f"🔍 为插件 {namespace} 添加依赖路径: {dependencies_dir}")

            # 遍历依赖目录中的所有子目录
            for item in dependencies_dir.iterdir():
                if item.is_dir():
                    # 添加到系统路径
                    sys.path.insert(0, str(item))
                    added_paths.append(str(item))

                    # 对于 Windows 系统，将 .libs 目录添加到 PATH
                    if sys.platform == "win32":
                        libs_path = item / ".libs"
                        if libs_path.exists() and libs_path.is_dir():
                            os.environ["PATH"] = str(libs_path) + os.pathsep + os.environ["PATH"]
                            added_paths.append(str(libs_path))

            # 保存添加的路径，以便卸载时移除
            self.dependency_paths[namespace] = added_paths

    def _remove_dependencies_from_path(self, namespace: str):
        """从系统路径中移除插件的依赖"""
        if namespace in self.dependency_paths:
            for path in self.dependency_paths[namespace]:
                # 从 sys.path 中移除
                if path in sys.path:
                    sys.path.remove(path)
                    print(f"➖ 移除依赖路径: {path}")

                # 对于 Windows 系统，从 PATH 中移除 .libs 目录
                if sys.platform == "win32" and ".libs" in path:
                    path_var = os.environ["PATH"]
                    if path in path_var:
                        new_path = path_var.replace(path + os.pathsep, "").replace(path, "")
                        os.environ["PATH"] = new_path

            # 清理记录
            del self.dependency_paths[namespace]

    def _load_single_plugin(self, plugin_path: Path):
        """
        加载单个插件

        :param plugin_path: 插件路径
        """

        plugin_dir = Path(plugin_path)

        meta = Package(plugin_dir)

        namespace = meta.get("name", None)
        author = meta.get("author", "null")

        if not namespace:
            return

        if namespace in self.plugins:
            return

        package_name = f"plugin_{namespace}"

        if package_name in sys.modules:
            return

        # 添加依赖路径到系统路径
        self._add_dependencies_to_path(plugin_dir, namespace)

        try:
            with ModuleLoader(plugin_dir, package_name, "main.py") as module:
                main_module = module

                # ===== 新增：加载并处理 func.py =====
                func_file = plugin_dir / "func.py"
                if func_file.exists():
                    # 处理 func.py 中的函数
                    self._process_func_functions(
                        func_file,
                        main_module,
                        self.app,  # 传入 app 实例
                    )
                # ===== 新增结束 =====

        except Exception as e:
            # 加载失败时移除依赖路径
            self._remove_dependencies_from_path(namespace)
            raise e

        # 创建并存储 PluginConfig 实例
        plugin = Plugin(
            namespace=namespace,
            path=plugin_path,
            author=author,
            module=main_module,
            package_name=package_name,
            meta=meta.file
        )

        if not self.app.plugin_data.get(namespace, True, "action"):
            plugin.disable()

        self.plugins[namespace] = plugin
        self.package_paths[package_name] = str(plugin_dir)

        print(f"✅ 插件加载成功: {namespace} by {author}")

    def _process_func_functions(self, func_file: Path, main_module, app):
        """
        处理 func.py 中的函数，替换为内置实现

        :param func_file: func.py 文件路径
        :param main_module: 插件主模块
        :param app: 应用实例
        """
        # 使用AST解析函数名
        try:
            with open(func_file, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            print(f"⚠️ 无法读取 func.py: {e}")
            return

        function_names = []
        try:
            tree = ast.parse(source)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    function_names.append(node.name)
        except Exception as e:
            print(f"⚠️ 解析 func.py 的AST失败: {e}")
            return

        if not function_names:
            return

        # 注入内置函数实现
        for func_name in function_names:
            # 检查是否已注册该函数
            if func_name in self.function_registry:
                # 获取内置函数实现
                func_impl = self.function_registry[func_name]

                # 创建自动传入 app 的包装函数
                def make_wrapper(_f: Callable) -> Callable:
                    def wrapper(*args, **kwargs) -> Any:
                        return _f(app, *args, **kwargs)

                    # 显式设置类型和文档
                    wrapper.__name__ = _f.__name__
                    wrapper.__doc__ = _f.__doc__ if hasattr(_f, '__doc__') else None
                    # 添加类型注释
                    wrapper.__annotations__ = getattr(_f, '__annotations__', {})
                    # 添加原始函数的元数据
                    wrapper.__original_function = _f  # type: ignore
                    return wrapper

                wrapped_func = make_wrapper(func_impl)

                # 使用 cast 确保类型检查器理解这是一个可调用对象
                setattr(main_module, func_name, cast(Callable, wrapped_func))

    def run_hook(self, namespace: str, hook_name: str, *args, **kwargs) -> Any:
        """
        执行指定插件的钩子函数

        :param namespace: 插件命名空间
        :param hook_name: 钩子名称（不需要带 _hook 后缀）
        :param args: 传递给钩子函数的参数
        :param kwargs: 传递给钩子函数的关键字参数
        :return: 钩子函数的返回值
        """
        if namespace in self.plugins:
            return self.plugins[namespace].run_hook(hook_name, *args, **kwargs)

        print(f"插件未加载: {namespace}")
        return None

    def run_hook_all(self, hook_name: str, *args, **kwargs) -> list[Any]:
        if not self.plugins: return []

        return [n.run_hook(hook_name, *args, **kwargs) for n in self.plugins.values()]

    def get_plugin(self, namespace: str) -> Optional[Plugin]:
        """
        获取插件实例

        :param namespace: 插件命名空间
        :return: PluginConfig 实例或 None
        """
        return self.plugins.get(namespace)

    def list_plugins(self) -> list[Plugin]:
        """
        列出所有已加载插件的命名空间

        :return: 插件命名空间列表
        """
        return list(self.plugins.values())

    def unload_plugin(self, namespace: str):
        """
        卸载指定插件

        :param namespace: 插件命名空间
        """
        if namespace in self.plugins:
            plugin = self.plugins[namespace]
            package_name = plugin.package_name

            # 清理所有相关模块
            to_remove = [name for name in sys.modules
                         if name == package_name or name.startswith(f"{package_name}.")]

            for module_name in to_remove:
                del sys.modules[module_name]

            # 移除依赖路径
            self._remove_dependencies_from_path(namespace)

            # 清理插件记录
            del self.plugins[namespace]
            if package_name in self.package_paths:
                del self.package_paths[package_name]

            print(f"✅ 插件已卸载: {namespace}")

            self.app.plugin_data.update_state()
        else:
            print(f"⚠️ 插件未加载: {namespace}")

    def enable(self, namespace: str):
        self.get_plugin(namespace).enable()

    def disable(self, namespace: str):
        self.get_plugin(namespace).disable()