from pathlib import Path

from vebp.libs.string import get_fs


def get_f_string(src):
    if not isinstance(src, str):
        return src

    return get_fs(src, {
        "cwd": Path.cwd(),
        "PYTHON": ...
    }, "$")