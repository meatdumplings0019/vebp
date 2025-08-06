from vebp.libs.color import print_red


def set_command(args, app):
    def verification(key, *ks) -> bool:
        return app.settings.get(key, None, *ks) is None

    arg = getattr(args, "args", [])
    if len(arg) < 2:
        raise IndexError("必须有键名和值!")

    keys = arg[0].split(".")
    values = arg[1:]

    if verification(keys[0], *keys[1:]):
        raise KeyError(f"{arg[0]} 不存在")
    try:
        app.settings.write(keys[0], values[0] if len(values) <= 1 else values.copy(), *keys[1:])
        print(f'已将 {arg[0]} 修改为 { values[0] if len(values) <= 1 else values.copy()} ')
    except Exception as e:
        print_red(f'修改失败 {e}')