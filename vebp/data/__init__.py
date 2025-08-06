from typing import Any

from vebp.fstring import get_f_string
from vebp.libs.file.json import JsonStream
from vebp.libs.path import MPath
from vebp.libs.types import path_type


class BaseData:
    FILENAME = "vebp.json"

    PROPERTY = {}

    def __init__(self, path: path_type = ".") -> None:
        self.path = MPath.to_path(path) / self.FILENAME
        self.file = {}

        self._read_value()

    def _read_value(self) -> None:
        fs = JsonStream(self.path)
        value: dict

        try:
            value = fs.read()
        except FileNotFoundError:
            value = {}

        self.file = value.copy()

    def generate_default(self) -> dict:
        generate = {}

        for k, v in self.PROPERTY.items():
            value = v.get("default", None)
            if value is not None:
                generate[k] = get_f_string(value)

        return generate

    def create(self, path: path_type = ".", overwrite=False) -> bool:
        fs = JsonStream(MPath.to_path(path) / self.FILENAME)

        if fs.exists and not overwrite:
            self.verification()
            print(f"{fs} 已存在。使用 --force 覆盖。")
            return False

        fs.create()
        data = self.generate_default()
        fs.write(data)

        self._read_value()

        print(f"成功创建 {fs}!")

        return True

    def get(self, key, default=None, *keys) -> Any:
        try:
            if not keys:
                return self.file.get(key, default)

            value = self.file.get(key, {})

            for k in keys[1:-1]:
                value = value.get(k, {})

            return value.get(keys[-1], default)
        except Exception as e:
            print(f"🔥{e}")
            return None

    def write(self, key, value, *keys) -> None:
        def _write(d, ks, v):
            if not ks: return v
            tmp = d.copy()
            tmp[ks[0]] = value if len(ks) <= 1 else _write(tmp.get(ks[0], {}), ks[1:], v)
            return tmp

        self.file = _write(self.file, [key, *keys], value).copy()

        try:
            f = JsonStream(self.path)
            f.write(self.file)
        except Exception as e:
            print(f"写入配置文件失败: {e}")

    def delete(self, *keys):
        if len(keys) <= 1:
            del self.file[keys[0]]
            f = JsonStream(self.path)
            f.write(self.file)

        value: dict = self.get(keys[0], {}, *keys[1:-1])

        del value[keys[-1]]

        self.write(keys[0], value, *keys[1:-1])

    def verification(self):
        self._read_value()

        self.file = {
            **self.generate_default(),
            **self.file
        }

        try:
            f = JsonStream(self.path)
            f.write(self.file)
        except Exception as e:
            print(f"写入配置文件失败: {e}")