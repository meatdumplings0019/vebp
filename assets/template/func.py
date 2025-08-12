"""
预定义函数, 使用相对导入.
"""

# noinspection PyPropertyDefinition
class FileStream:
    def __init__(self, path):
        pass

    @property
    def name(self):
        pass

    @property
    def path(self):
        pass

    @property
    def exists(self):
        pass

    @property
    def suffix(self):
        pass

    def read(self):
        pass

    def write(self, text: str):
        pass

    def create(self, value: str = ""):
        pass

    def copy(self, destination, ignore=None):
        pass

    def delete(self):
        pass


# noinspection PyPropertyDefinition
class JsonStream(FileStream):
    @property
    def is_json(self) -> bool:
        pass

    def read(self):
        pass

    def write(self, data: dict, indent=4):
        pass


# noinspection PyPropertyDefinition
class FolderStream:
    def __init__(self, path):
        pass

    @property
    def name(self):
        pass

    @property
    def path(self):
        pass

    @property
    def exists(self):
        pass

    def copy(self, destination, ignore=None):
        pass

    def delete(self):
        pass

    def create(self):
        pass

    def walk(self):
        pass


def get_assets_path(namespace: str):
    """
    返回某个插件的资源地址
    """
    pass

def get_data_path(namespace: str):
    """
    返回某个插件的数据地址
    """
    pass