import re
from pathlib import Path

from vebp.console import ConsoleInput, Choice
from vebp.libs.file import FolderStream
from vebp.libs.func import smart_call


class CreateObject:
    def __init__(self, name, main_func, assets_path):
        self.name = name
        self.main_func = main_func
        self.assets_path = assets_path

        self.table = ConsoleInput()

        self._add_default()

    def _add_default(self):
        self.add_input_table(
            "name",
            "请输入项目名称",
            "project",
            lambda x: True if re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", x) else "项目名称必须以字母开头，只能包含字母、数字、下划线和连字符",
            True,
            "项目名称"
        )

    def add_input_table(self, key, prompt, default = None, validate = None, required = True, description = ""):
        self.table.add_question(
            key=key,
            question_type="input",
            prompt=prompt,
            default=default,
            validate=validate,
            required=required,
            description=description
        )

    def add_confirm_table(self, key, prompt, default = True, required = True, description = ""):
        self.table.add_question(
            key=key,
            question_type="confirm",
            prompt=prompt,
            default=default,
            required=required,
            description=description
        )

    def add_select_table(self, key, prompt, choices: dict, description = ""):
        choices_obj = []

        for name, choice in choices.items():
            choices_obj.append(Choice(name, choice[0], choice[1]))

        self.table.add_question(
            key=key,
            question_type="select",
            prompt=prompt,
            choices=choices_obj,
            description=description
        )

    def start(self):
        result = self.table.run()

        fs = FolderStream(Path.cwd() / result.name).create()
        FolderStream(self.assets_path).copy(fs)
        smart_call(self.main_func, self)

    def __repr__(self):
        return f"[CreateObject {self.name}]"