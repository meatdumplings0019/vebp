import re
import subprocess
from pathlib import Path

from vebp.config import mirror_url
from vebp.data.package import Package
from vebp.libs.color import print_red
from vebp.libs.system import SystemConsole
from vebp.libs.venvs.package import is_package_installed
from vebp.libs.venvs.pip import pip_command
from vebp.libs.venvs.version import get_package_version


class Installer:
    def __init__(self, app, path = Path.cwd()):
        self.path = path
        self.app = app

        self.package = Package(path)

    def _installed(self, packages):
        to_install = []

        for pkg in packages:
            match = re.match(r"([a-zA-Z0-9_-]+)(.*)", pkg)
            if match:
                pkg_name = match.group(1)
                version_spec = match.group(2).strip()
                if not version_spec:
                    version = self.package.get_dependencies(pkg_name)
                    if version:
                        version_spec = f"=={version}"
                    else:
                        version_spec = ""

                to_install.append(f"{pkg_name}{version_spec}")
            else:
                raise ValueError(f"{pkg} is not a valid package name")

        return to_install

    def install(self, packages, write: bool = True):
        url = self.package.get("url", self.app.settings.get_value("mirror_url", mirror_url))

        to_install = self._installed(packages)

        total = len(to_install)

        def _install(pkgs):
            tmp = pkgs.copy()
            new = []

            for p in pkgs:
                if is_package_installed(p):
                    try:
                        version = p.split("==")[1]
                        if version == get_package_version(p):
                            new.append(p)
                            tmp.remove(p)
                    except IndexError:
                        new.append(p)
                        tmp.remove(p)

            return tmp, new

        to_install, new_install = _install(to_install)

        installed = len(to_install)

        if installed > 0:
            cmd = [
                *pip_command(self.package.get("venvs", ".venvs")),
                "install",
                *to_install,
                "-i",
                url
            ]

            try:
                print(f"共有 {total} 个包, 已安装 {total - installed} 个包, 将安装 {installed} 个包")
                SystemConsole.execute(cmd, capture_output=True, check=True)
                print(f"安装完成, 已安装 {", ".join([i.split("==")[0] for i in to_install])}")
            except subprocess.CalledProcessError:
                print_red("发生错误.")
                return
        else:
            print(f"未安装任何包")

        if write:
            for pkg in [*[i.split("==")[0] for i in to_install], *new_install]:
                self.package.write("dependencies", get_package_version(pkg), pkg)

    def for_package(self):
        self.install(self.package.dependencies.keys(), False)

    def uninstall(self, packages):
        to_uninstall = self._installed(packages)

        total = len(to_uninstall)

        cmd = [
            *pip_command(self.package.get("venvs", ".venvs")),
            "uninstall",
            *to_uninstall,
            "-y"
        ]

        try:
            print(f"将卸载 {total} 个包.")
            SystemConsole.execute(cmd, capture_output=True, check=True)
            print(f"卸载完成, 已卸载 {", ".join([i.split("==")[0] for i in to_uninstall])}")
        except subprocess.CalledProcessError as e:
            print_red(f"发生错误, 错误码为{e.returncode}.")
            return

        for pkg in [i.split("==")[0] for i in to_uninstall]:
            if not self.package.get_dependencies(pkg) is None:
                self.package.delete("dependencies", pkg)