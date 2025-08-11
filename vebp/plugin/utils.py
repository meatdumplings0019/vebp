from vebp.libs.file import FileStream, FolderStream


def copy_func_file(app, file):
    fs = FileStream(app.template / "func.py")
    file = FolderStream(file).create()

    t = FolderStream(file.path / "func.py")
    if t:
        t.delete()

    if not fs.exists:
        raise FileNotFoundError(f"模板不完整")

    fs.copy(file)