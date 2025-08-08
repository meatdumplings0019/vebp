from pathlib import Path

from vebp.data.build_config import BuildConfig
from vebp.data.package import Package


def init_command(args, app):
    path = Path(getattr(args, "path", Path.cwd()))

    print(f"🛠️ 正在初始化 vebp 插件...")
    print()

    package = Package(path)
    build_config = BuildConfig(path)

    package.create(path, args.force)
    build_config.create(path, args.force)
    app.settings.config.create(path, args.force)

    package.write("name", path.name if path.name else Path.cwd().name)