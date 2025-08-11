from typing import Any

from vebp.core import DataCore
from vebp.registry import Registry


class Plugin(DataCore):
    def __init__(self, namespace: str, path, author: str, module: Any, package_name: str, meta: dict[str, Any]):
        """
        插件类封装

        :param namespace: 插件命名空间
        :param author: 插件作者
        :param module: 插件主模块
        :param package_name: 插件包名
        :param meta: 插件元数据
        """
        super().__init__(namespace, path)
        self._author = author
        self.module = module
        self.package_name = package_name
        self.meta = meta

        self._action = True

    @property
    def author(self) -> str:
        return self._author

    @property
    def action(self):
        return self._action

    def run(self, hook_name: str, suffix: str, *args, **kwargs) -> Any:
        """
        执行函数

        :param hook_name: 钩子名称
        :param suffix: 后缀名称
        :param args: 传递给钩子函数的参数
        :param kwargs: 传递给钩子函数的关键字参数
        :return: 钩子函数的返回值
        """

        if not self._action:
            return None

        hook_func_name = f"{hook_name}_{suffix}"

        if not hasattr(self.module, hook_func_name):
            print(f"插件 {self._namespace} 未定义钩子函数: {hook_func_name}")
            return None

        hook_func = getattr(self.module, hook_func_name)

        if not callable(hook_func):
            raise TypeError(f"插件 {self._namespace} 的 {hook_func_name} 不是可调用函数")

        try:
            return hook_func(self.namespace, *args, **kwargs)
        except Exception as e:
            print(f"⚠️ 钩子执行失败 [{self._namespace}.{hook_func_name}]: {str(e)}")
            raise

    def run_hook(self, hook_name: str, *args, **kwargs) -> Any:
        """
        执行插件的钩子函数

        :param hook_name: 钩子名称（不需要带 _hook 后缀）
        :param args: 传递给钩子函数的参数
        :param kwargs: 传递给钩子函数的关键字参数
        :return: 钩子函数的返回值
        """

        return self.run(hook_name, "hook", *args, **kwargs)

    def register(self, register_name: str, *args, **kwargs) -> Registry:
        return Registry(self.run(register_name, "register", *args, **kwargs))

    def get_meta(self) -> dict[str, Any]:
        """获取插件元数据"""
        return self.meta.copy()

    def enable(self):
        self._action = True

    def disable(self):
        self._action = False