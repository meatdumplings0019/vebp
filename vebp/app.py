from vebp.add import add_command
from vebp.clitool import CliTool
from vebp.core import Core
from vebp.libs.color import print_red
from vebp.libs.path import MPath
from vebp.libs.system.key_exit import wait_for_any_key
from vebp.libs.venvs.python_venv import is_python
from vebp.plugin.manager import PluginManager
from vebp.version import __version__


class App(CliTool, Core):
    def __init__(self):
        super().__init__("vebp", __version__, "python build and package tool.")
        super(CliTool, self).__init__("vebp", MPath.get())
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all_plugin()

        self.python_version = None

        add_command(self)

    @property
    def template(self):
        return self.assets / "template"

    def run(self):
        has, self.python_version, cmd = is_python()

        if not has:
            print_red("你的电脑并没有安装python环境")
            wait_for_any_key()

        self.plugin_manager.run_hook_all("test")
        super().run()