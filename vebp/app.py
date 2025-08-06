from colorama import Fore, Style

from vebp.add import add_command
from vebp.clitool import CliTool
from vebp.core import Core
from vebp.libs.color import print_red
from vebp.libs.system.key_exit import wait_for_any_key
from vebp.libs.venv.python_venv import is_python
from vebp.plugin.manager import PluginManager
from vebp.version import __version__


class App(CliTool, Core):
    def __init__(self):
        super().__init__("vebp", __version__, "python build and package tool.")
        super(CliTool, self).__init__()
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all_plugin()

        add_command(self)

    def run(self):
        has, version, _ = is_python()

        if not has:
            print_red("你的电脑并没有安装python环境")
            wait_for_any_key()

        print(f"Python版本: {Fore.CYAN}{version}{Style.RESET_ALL}")

        super().run()