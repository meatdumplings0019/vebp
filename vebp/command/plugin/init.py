import re
from pathlib import Path

from vebp.console import ConsoleInput
from vebp.data.plugin_config import PluginConfig
from vebp.libs.path import MPath
from vebp.plugin.init import plugin_init
from vebp.plugin.utils import copy_func_file


def plugin_init_command(args, app):
    path = MPath.to_path(getattr(args, "path", Path.cwd()))

    if getattr(args, "yes", False):
        plugin_init(app, path.name if path.name else Path.cwd().name, app.settings.get("author", "author"), "1.0.0", path)
        copy_func_file(app, path)

        return

    form = ConsoleInput()

    form.add_question(
        key="name",
        question_type="input",
        prompt="请输入项目名称",
        default=path.name if path.name else Path.cwd().name,
        validate=lambda x: True if re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$",
                                            x) else "项目名称必须以字母开头，只能包含字母、数字、下划线和连字符",
        required=True,
        description="项目名称"
    )

    form.add_question(
        key="author",
        question_type="input",
        prompt="请输入作者名称",
        default=app.settings.get("author", "author"),
        validate=lambda x: True if re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$",
                                            x) else "作者名称必须以字母开头，只能包含字母、数字、下划线和连字符",
        required=True,
        description="项目名称"
    )

    form.add_question(
        key="version",
        question_type="input",
        prompt="请输入版本",
        default="1.0.0",
        required=True,
        description="项目名称"
    )

    result = form.run()

    plugin_init(app, result.name, result.author, result.version, path)

    copy_func_file(app, path)
