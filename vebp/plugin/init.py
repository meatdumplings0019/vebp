from vebp.data.package import Package
from vebp.libs.file import FolderStream
from vebp.libs.types import path_type


def plugin_init(app, name: str, author: str, version: str, to_path: path_type):
    source = FolderStream(app.template / "plugin")
    fs = FolderStream(to_path).create()

    source.copy(fs)

    package = Package(fs)

    package.write("name", name)
    package.write("author", author)
    package.write("version", version)