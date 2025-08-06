from typing import Any

from vebp.config import mirror_url
from vebp.data import BaseData
from vebp.data.config import Config
from vebp.libs.file.json import JsonStream


class Settings(BaseData):
    FILENAME = "settings.json"

    PROPERTY = {
        "mirror_url": {
            "config": False,
            "default": mirror_url,
        }
    }

    def __init__(self, path):
        super().__init__(path)
        self.config = Config()
        self._update_config(self.config)

    def _update_config(self, cfg):
        tmp = {}

        for k, v in self.PROPERTY.items():
            if v.get("config", False):
                t = v.copy()
                del t["config"]

                tmp[k] = t

        cfg.PROPERTY = {
            **cfg.PROPERTY,
            **tmp
        }

    def create(self, **kwargs) -> bool:
        fs = JsonStream(self.path)

        if fs.exists:
            self.verification()
            return False

        fs.create()
        data = self.generate_default()
        fs.write(data)

        self._read_value()

        return True

    def get_value(self, key, default=None, *keys) -> Any:
        settings_value = self.get(key, default, *keys)
        return self.config.get(key, settings_value, *keys)