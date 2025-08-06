from pathlib import Path

from vebp.data.build_config import BuildConfig
from vebp.data.package import Package
from vebp.plugin.data import PluginData
from vebp.settings import Settings
from vebp.libs.file import FolderStream


class Core:
    def __init__(self):
        self.home = Path.home()

        self.package = Package()
        self.build_config = BuildConfig()
        self.settings = Settings(self.main)
        self.plugin_data = PluginData(self.plugins, self)

        self.init()

    def init(self):
        dct = {
            "files": [
                self.settings,
                self.plugin_data,
            ],
            "folders": [
                FolderStream(self.main),
                FolderStream(self.global_),
                FolderStream(self.plugins)
            ]
        }

        for folder in dct['folders']:
            folder.create()

        for file in dct['files']:
            file.create()

    @property
    def main(self) -> Path:
        return self.home / '.vebp'

    @property
    def global_(self) -> Path:
        return self.main / "global"

    @property
    def plugins(self) -> Path:
        return self.main / "plugins"