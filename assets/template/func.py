"""
预定义函数, 使用相对导入.
"""

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


def get_fs(src: str, context: dict, spl: str="$") -> str:
    """
    解析自定义 f 字符串格式：
    - $name 替换为字典中的值
    - $$ 转义为单个 $
    - 未识别的占位符保留原样

    :param src: 包含占位符的原始字符串
    :param context: 包含占位符键值对的字典
    :param spl:

    :return: 解析后的字符串
    """


def filter_null(lst: list) -> list:
    pass


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
