from vebp.libs.path import MPath
from vebp.libs.types import path_type


class DataCore:
    def __init__(self, namespace: str, path: path_type):
        self._namespace = namespace
        self._path = MPath.to_path(path)

    @property
    def namespace(self):
        return self._namespace

    @property
    def path(self):
        return self._path

    @property
    def assets(self):
        return self.path / "assets"

    @property
    def data(self):
        return self.path / "data"