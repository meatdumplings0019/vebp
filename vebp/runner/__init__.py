import subprocess
import sys
from pathlib import Path

from vebp.data.package import Package
from vebp.libs.color import print_red
from vebp.libs.venv import venv_path


class Runner:
    _builtin_mappings = {
    }

    _plugin_mappings = {}

    def __init__(self, app, command):
        self._builtin_mappings = {
            **self._builtin_mappings,
            "run": str(venv_path(app.package.get(".venv", ".venv")))
        }

        self.command = command

    def resolve_command(self, command_str):
        parts = command_str.strip().split()
        if not parts:
            return command_str

        command_head = parts[0]
        resolved = self._plugin_mappings.get(
            command_head,
            self._builtin_mappings.get(command_head, command_head)
        )

        return [resolved] + parts[1:]


    def get_available_commands(self):
        return {
            **self._builtin_mappings,
            **self._plugin_mappings
        }

    def run(self):
        try:
            package = Package()
            scripts = package.get("scripts", {})

            if self.command not in scripts:
                print_red(f"❌ 错误: 未找到脚本 '{ self.command}'")

                raise

            command_str = scripts[self.command]
            print(f"🚀 执行脚本: {self.command}")

            # 解析命令映射
            resolved_command = self.resolve_command(command_str)

            print(f"📜 命令: {' '.join(resolved_command)}")

            print("")

            subprocess.run(
                resolved_command,
                shell=True,
                cwd=Path.cwd(),
            )

        except FileNotFoundError:
            print_red(f"❌ 错误: 未找到 {Package.FILENAME} 文件")
            print("👉 请先运行 'vebp init' 创建配置文件")
            sys.exit(1)
        except Exception as e:
            print_red(f"❌ 执行错误: {str(e)}")
            sys.exit(1)