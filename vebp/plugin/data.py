from vebp.data import BaseData
from vebp.libs.file.json import JsonStream


class PluginData(BaseData):
    FILENAME = "plugins.json"

    def __init__(self, path, app):
        super().__init__(path)
        self.app = app

    def update_state(self):
        self._read_value()

        tmp = {}

        for k, v in self.app.plugin_manager.plugins.items():
            if k in list(self.file.keys()):
                tmp[k] = self.file[k]
            else:
                tmp[k] = {
                    "action": v.action,
                }

        self.file = tmp.copy()

        fs = JsonStream(self.path)
        fs.write(self.file)

    def create(self, **kwargs) -> bool:
        fs = JsonStream(self.path)

        if fs.exists:
            return False

        fs.create()
        data = self.generate_default()
        fs.write(data)

        self._read_value()

        return True