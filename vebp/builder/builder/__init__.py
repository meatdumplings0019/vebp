import platform
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Union, Optional

from vebp.builder import BaseBuilder
from vebp.config import build_name
from vebp.data.build_config import BuildConfig
from vebp.data.package import Package
from vebp.libs.color import print_red
from vebp.libs.file import FileStream, FolderStream
from vebp.libs.string import get_fs
from vebp.libs.system import SystemConsole
from vebp.libs.venvs import venv_path


class Builder(BaseBuilder):
    def __init__(self, app, name=None, icon=None, parent_path=None, sub=None, base_path=".") -> None:
        super().__init__(app, name, base_path)
        self._icon = Path(icon) if icon else None
        self._console = False
        self._onefile = True
        self._assets: Dict[str, list[Path]] = {}
        self._in_assets: Dict[str, list[Path]] = {}
        self._sub = sub
        self._parent_path = parent_path
        self._exclude_modules = []
        self._exclude_commands = []
        self._before_events = []

        self._auto_run = True

        self.sub_project_src = {}
        self.sub_project_builder = []

    def _get_path(self) -> None:
        if not self._parent_path:
            self._parent_path = self.name

        self._project_dir = self.base_output_dir / self._parent_path

        if self._sub:
            self._project_dir /= self._sub

    @property
    def icon(self) -> Path:
        return self._icon

    @property
    def console(self) -> bool:
        return self._console

    @property
    def onefile(self) -> bool:
        return self._onefile

    @property
    def assets(self) -> Dict[str, list[Path]]:
        return self._assets

    @property
    def in_assets(self) -> Dict[str, list[Path]]:
        return self._in_assets

    @property
    def auto_run(self) -> bool:
        return self._auto_run

    @auto_run.setter
    def auto_run(self, value) -> None:
        self._auto_run = value

    @staticmethod
    def from_package(app, folder_path = None, sub=None, parent=None, base_path=".") -> Optional["Builder"]:
        if folder_path:
            folder_path = Path(str(folder_path))
            build_config = BuildConfig(folder_path)
            package_config = Package(folder_path)
        else:
            build_config = BuildConfig()
            package_config = Package()

        if not build_config or not package_config:
            return None

        builder = Builder(app, package_config.get('name', None), sub=sub, parent_path=parent, base_path=base_path)
        builder.venv = package_config.get('venv', '.venv')

        builder.set_script(package_config.get('main', None))
        builder.set_console(build_config.get('console', False))

        icon = build_config.get('icon', None)
        if icon:
            builder._icon = Path(icon)

        onefile = build_config.get('onefile', True)
        builder.set_onefile(onefile)

        assets_lst = build_config.get('assets', [])
        if assets_lst:
            for asset in assets_lst:
                builder.add_assets(asset.get("from", []), asset.get("to", "."))

        in_assets_lst = build_config.get('in_assets', [])
        if in_assets_lst:
            for asset in in_assets_lst:
                builder.add_in_assets(asset.get("from", []), asset.get("to", "."))

        sub_pro = build_config.get('sub_project', [])
        if sub_pro:
            for pro in sub_pro:
                builder.add_sub_project(pro.get("path", "sub_project"), pro.get("script", None))
        exclude_modules = build_config.get('exclude_modules', [])
        builder._exclude_modules = exclude_modules

        auto_run = build_config.get('auto_run', True)
        builder.auto_run = auto_run

        exclude_commands = build_config.get('exclude_commands', [])
        builder._exclude_commands = exclude_commands

        before_events = build_config.get('before_events', [])
        builder._before_events = before_events

        return builder

    def set_console(self, console) -> "Builder":
        if console:
            self._console = console
        return self

    def set_onefile(self, onefile) -> "Builder":
        if onefile:
            self._onefile = onefile
        return self

    def add_assets(self, sources: list[Union[str, Path]], target_relative_path: str = "") -> "Builder":
        if not sources:
            return self

        source_paths = [Path(source) for source in sources]

        self.assets.setdefault(target_relative_path, [])

        for source in source_paths:
            source = self._base_path / source
            if not source.exists():
                print_red(f"警告: 资源源不存在: {source}")
            else:
                self.assets[target_relative_path].append(source)

        return self

    def add_in_assets(self, sources: list[Union[str, Path]], target_relative_path: str = "") -> "Builder":
        if not sources:
            return self

        source_paths = [Path(source) for source in sources]

        self.in_assets.setdefault(target_relative_path, [])

        for source in source_paths:
            source = self._base_path / source
            if not source.exists():
                print_red(f"警告: 内部资源源不存在: {source}")
            else:
                self.in_assets[target_relative_path].append(source)

        return self

    def add_sub_project(self, key, package_path) -> "Builder":
        if package_path:
            self.sub_project_src[key] = package_path

        return self

    def _validate(self) -> bool:
        super()._validate()

        if not self.script_path or not self.script_path.is_file():
            raise ValueError(f"脚本文件不存在: {self.script_path}")

        if self.icon and not self.icon.is_file():
            raise ValueError(f"图标文件不存在: {self.icon}")

        return True

    def _get_add_data_args(self) -> list[str]:
        add_data_args = []
        separator = ";" if platform.system() == "Windows" else ":"

        for target_relative, sources in self.in_assets.items():
            for source in sources:
                abs_source = source.resolve()

                out = Path(target_relative)

                if source.is_dir():
                    out /= source

                arg = f"{abs_source}{separator}{out}"
                add_data_args.extend(["--add-data", arg])

        return add_data_args

    def _copy_assets(self) -> bool:
        if not self._assets:
            return True

        print("\n📦 复制外部资源...")
        success = True

        for target_relative, sources in self.assets.items():
            target_path = self._project_dir / target_relative

            for source in sources:
                target_folder = FolderStream(str(target_path / source))
                FolderStream(source).copy(target_folder)

        return success

    def _print_result(self, target_path) -> None:
        print(f"\n🎉 项目构建成功!")
        print(f"📂 输出目录: {self._project_dir}")
        print(f"📦 输出文件: {target_path}")
        print(f"📦 单文件打包: {'✅' if self.onefile else '❌'}")
        print(f"🖥️ 显示控制台: {'✅' if self.console else '❌'}")
        print(f"🚀 自动运行: {'✅' if self.auto_run else '❌'}")

    def _start_build(self, cmd) -> None:
        print(f"\n🔨 开始打包项目: {self.name}")
        print(f"📜 脚本路径: {self.script_path}")
        print(f"📦 单文件打包: {'✅' if self.onefile else '❌'}")
        print(f"🖥️ 显示控制台: {'✅' if self.console else '❌'}")
        print(f"🚀 自动运行: {'✅' if self.auto_run else '❌'}")

        if self.in_assets:
            print("📦 要嵌入的内部资源:")
            for target_relative, sources in self.in_assets.items():
                for source in sources:
                    print(f"  ➡️ {source} -> {target_relative}")

        print("⏳ 打包进行中...")

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            check=True
        )

    def _get_cmd(self, python_path) -> list[str]:
        cmd = [str(python_path).strip(), '-m', 'PyInstaller', '--noconfirm']

        if self.onefile:
            cmd.append('--onefile')
        else:
            cmd.append('--onedir')

        if not self.console:
            cmd.append('--noconsole')

        if self.icon:
            cmd.extend(['--icon', str(self.icon.resolve())])

        if self._exclude_modules:
            for module in self._exclude_modules:
                cmd.extend(['--exclude-module', module])

        cmd.extend(self._get_add_data_args())
        cmd.extend(['--name', self.name, str(self.script_path.resolve())])
        cmd.extend(self._exclude_commands)

        return cmd

    @staticmethod
    def _run_executable(exe_path: Path) -> None:
        try:
            if not exe_path.exists():
                print_red(f"❌ 可执行文件不存在: {exe_path}")
                return

            print(f"🚀 启动程序: {exe_path}")
            if platform.system() == 'Windows':
                subprocess.Popen([str(f"{exe_path}")], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([str(exe_path)])
        except Exception as e:
            print_red(f"运行程序失败: {str(e)}")

    def _compile_sub_project(self) -> None:
        if not self.sub_project_src:
            return

        for key, pro in self.sub_project_src.items():
            self.sub_project_builder.append(self.from_package(self.app, pro, key, self._project_dir, pro))

    def _build_sub_project(self) -> None:
        for pro in self.sub_project_builder:
            pro.build()

    def _run_before_events(self) -> None:
        dct = {
            "DIR": self._project_dir
        }

        for event in self._before_events:
            cmd = get_fs(event, dct).split()
            try:
                match cmd[0]:
                    case "copy":
                        FolderStream(cmd[1]).copy(cmd[2])
                    case _:
                        SystemConsole.execute(cmd)
            except Exception as e:
                print_red(f"{e}")

    def build(self) -> bool:
        self._get_path()

        python_path = venv_path(self.venv)

        FolderStream(str(self._project_dir)).create()

        try:
            self._validate()
            self._compile_sub_project()
            self._build_sub_project()
            self._start_build(self._get_cmd(python_path))

            if self.onefile:
                source_path = Path('dist') / f"{SystemConsole.exe(self.name)}"
            else:
                source_path = Path('dist') / self.name

            copy = FileStream(source_path).copy(self._project_dir)

            run_path = self._project_dir / f"{SystemConsole.exe(self.name)}"

            self._print_result(run_path)
            assets = self._copy_assets()

            if not self._sub and self._auto_run:
                print(f"\n🚀 正在启动应用程序...")
                self._run_executable(run_path)

            print("✅ 打包成功")

            self._run_before_events()

            return copy and assets
        except subprocess.CalledProcessError as e:
            print("\n❌ ", end="")
            print_red(f"打包失败! 错误代码: {e.returncode}")
            return False
        except Exception as e:
            print("\n❌ ", end="")
            print_red(f"{str(e)}")
            return False

    @staticmethod
    def clean(app):
        try:
            print(f"\n🧹 正在清理构建文件...")
            shutil.rmtree(Builder(app).base_output_dir, ignore_errors=True)
            shutil.rmtree(Path.cwd() / "build", ignore_errors=True)
            shutil.rmtree(Path.cwd() / "dist", ignore_errors=True)
            print(f"✅ 清理成功, 已删除'{build_name}', 'build', 'dist'")
        except Exception as e:
            print_red(f"\n❌ {str(e)}")

    def __repr__(self):
        return f'<Builder name: {self.name}>'