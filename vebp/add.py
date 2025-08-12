from vebp.command.build import build_command
from vebp.command.create import create_command
from vebp.command.init import init_command
from vebp.command.install import install_command
from vebp.command.plugin import plugin_command
from vebp.command.plugin.build import plugin_build_command
from vebp.command.plugin.init import plugin_init_command
from vebp.command.plugin.install import plugin_install_command
from vebp.command.plugin.list import plugin_list_command
from vebp.command.plugin.uninstall import plugin_uninstall_command
from vebp.command.plugin.unload import plugin_unload_command
from vebp.command.plugin.update import plugin_update_command
from vebp.command.plugin.update.func import plugin_update_func_command
from vebp.command.python import python_command
from vebp.command.python.version import python_version_command
from vebp.command.runner import run_command
from vebp.command.setter import set_command
from vebp.command.uninstall import uninstall_command


def add_command(app):
    def init():
        app.add_command("init", "🛠️ 初始化项目配置")
        app.add_sub_argument("init", "path", default=".", nargs="?")
        app.add_sub_argument("init", "--yes", "-y", "store_true", default=False)
        app.add_sub_argument("init", "--force", "-f", "store_true", default=False)

        app.set_sub_main_func("init", init_command, app)
    def install():
        app.add_command("install", "💿 安装python包")
        app.add_sub_argument("install", "packages", nargs="+")

        app.set_sub_main_func("install", install_command, app)
    def uninstall():
        app.add_command("uninstall", "💿 卸载python包")
        app.add_sub_argument("uninstall", "packages", nargs="+")

        app.set_sub_main_func("uninstall", uninstall_command, app)
    def setter():
        app.add_command("set", "💿 设置")
        app.add_sub_argument("set", "args", nargs="+")

        app.set_sub_main_func("set", set_command, app)
    def build():
        app.add_command('build', _help='🔨 构建可执行文件')

        app.add_sub_argument("build", 'name', nargs='?', default=None,
                                  _help='📛 项目名称 (如果在 vebp-build.json 中定义了则为可选)')
        app.add_sub_argument("build", '--src', '-s',
                                  _help='📜 要打包的 Python 脚本路径 (如果在 vebp-build.json 中定义了则为可选)')

        app.add_sub_argument("build", '--icon', '-i',
                                  _help='🖼️ 应用程序图标 (.ico 文件)')
        app.add_sub_argument("build", '--console', '-c', action='store_true',
                                  _help='🖥️ 显示控制台窗口 (默认隐藏)')
        app.add_sub_argument("build", '--onedir', '-d', action='store_true',
                                  _help='📁 使用目录模式而不是单文件模式 (默认: 单文件)')

        app.add_sub_argument("build", '--asset', action='append',
                                  _help='📦 外部资源: "源路径;目标相对路径" (复制到输出目录)')
        app.add_sub_argument("build", '--in_asset', action='append',
                                  _help='📦 内部资源: "源路径;目标相对路径" (嵌入到可执行文件中)')

        app.set_sub_main_func("build", build_command, app)
    def plugin():
        def plugin_build(p):
            p.add_command("build", '🔨 构建插件')

            p.add_sub_argument("build", "path", _help="📂 插件路径")

            p.set_sub_main_func("build", plugin_build_command, app)
        def plugin_install(p):
            p.add_command('install', "💿 安装插件")

            p.add_sub_argument("install", "path", _help="📂 插件路径")

            p.set_sub_main_func("install", plugin_install_command, app)
        def plugin_uninstall(p):
            p.add_command('uninstall', "💿 卸载插件")

            p.add_sub_argument("uninstall", "name", _help="📂 插件名称")

            p.set_sub_main_func("uninstall", plugin_uninstall_command, app)
        def plugin_unload(p):
            p.add_command('unload', "💿 停止加载插件")

            p.add_sub_argument("unload", "name", _help="📂 插件名称")

            p.set_sub_main_func("unload", plugin_unload_command, app)
        def plugin_list(p):
            p.add_command('list', "💿 展示插件")

            p.set_sub_main_func("list", plugin_list_command , app)
        def plugin_init(p):
            p.add_command("init", "🛠️ 初始化插件")

            p.add_sub_argument("init", "path", default=".", nargs="?")
            p.add_sub_argument("init", "--yes", "-y", "store_true", default=False)

            p.set_sub_main_func("init", plugin_init_command, app)
        def plugin_update(p):
            def plugin_update_func(p2):
                p2.add_command("func", "🛠️ 更新func.py文件")

                p2.add_sub_argument("func", "path", _help="📂 插件路径")

                p2.set_sub_main_func("func", plugin_update_func_command, app)

            p.add_command("update", "🛠️ 更新插件")

            p.set_sub_main_func("update", plugin_update_command, app)

            plugin_update_func(p.get("update"))

        app.add_command("plugin", "🧩 PluginConfig Tool")

        app.set_sub_main_func("plugin", plugin_command, app)

        plugin_build(app.get("plugin"))
        plugin_install(app.get("plugin"))
        plugin_uninstall(app.get("plugin"))
        plugin_unload(app.get("plugin"))
        plugin_list(app.get("plugin"))
        plugin_init(app.get("plugin"))
        plugin_update(app.get("plugin"))
    def run():
        app.add_command("run", "🚀 运行 package 中定义的脚本")

        app.add_sub_argument("run", 'script', _help='📜 要运行的脚本名称')

        app.set_sub_main_func("run", run_command, app)
    def python():
        def python_version(p):
            p.set_sub_main_func("version", python_version_command, app)

        app.add_command("python", "🧩 Python tool")

        app.add_sub_argument("python", '--version', '-v', action='store_true',
                             _help='ℹ️ 显示Python版本信息')

        app.set_sub_main_func("python", python_command, app)

        app.add_sub_command("python", "version", 'ℹ️ 显示Python版本信息')

        python_version(app.get("python"))
    def create():
        app.add_command("create", "🧩 tool")

        app.add_sub_argument("create", 'name', nargs="?", _help='📜 名称')

        app.set_sub_main_func("create", create_command, app)

    init()
    install()
    uninstall()
    setter()
    build()
    plugin()
    run()
    python()
    create()