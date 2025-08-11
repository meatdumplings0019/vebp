import re
from pathlib import Path

from vebp.console import ConsoleInput, Choice
from vebp.data.build_config import BuildConfig
from vebp.data.package import Package
from vebp.libs.file import FolderStream, FileStream


def init_command(args, app):
    def create(force, name, author, version):
        package = Package(path)
        build_config = BuildConfig(path)

        package.create(path, force)
        build_config.create(path, force)
        app.settings.config.create(path, force)

        package.write("name", name)
        package.write("author", author)
        package.write("version", version)

    path = Path(getattr(args, "path", Path.cwd()))

    fs = FolderStream(path).create()

    if getattr(args, "yes", False):
        print(f"🛠️ 正在初始化 vebp 项目...")
        print()

        create(args.force, path.name if path.name else Path.cwd().name, app.settings.get("author"), "1.0.0")

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

    form.add_question(
        key="force",
        question_type="confirm",
        prompt="是否覆盖配置?",
        default=False,
        description="覆盖现有的配置"
    )

    form.add_question(
        key="template",
        question_type="select",
        prompt="是否创建默认模板",
        choices=[
            Choice("none", None, "不选择"),
            Choice("common", "init", "默认模板"),
            Choice("high", "hinit", "高级模版")
        ],
        description="创建默认模板"
    )

    form.add_question(
        key="gitignore",
        question_type="confirm",
        prompt="是否创建.gitignore?",
        default=True,
        description="创建.gitignore"
    )

    form.add_question(
        key="README",
        question_type="confirm",
        prompt="是否创建README.md?",
        default=True,
        description="创建README.md"
    )

    result = form.run()

    if result.template:
        template = app.template / result.template

        fs.copy(template, fs)

        Package(path).write("name", result.name)
        Package(path).write("author", result.author)
        Package(path).write("version", result.version)

    else:
        create(result.force, result.name, result.author, result.version)

    if result.gitignore:
        FileStream(app.template / ".gitignore").copy(fs)

    if result.README:
        f = FileStream(fs.path / "README.md")
        f.copy(fs)
        f.write(f.read().format(name=result.name))

    print("创建成功!\n")