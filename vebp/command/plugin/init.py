from pathlib import Path

from vebp.libs.path import MPath
from vebp.plugin.init import plugin_init


def plugin_init_command(args, app):
    path = MPath.to_path(getattr(args, "path", Path.cwd()))

    plugin_init(app, path.name if path.name else Path.cwd().name, "author", "1", path)