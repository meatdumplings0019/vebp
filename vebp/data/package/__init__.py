from vebp.data import BaseData


class Package(BaseData):
    FILENAME = "vebp-package.json"

    PROPERTY = {
        "name": {
            "type": "str",
            "default": "name"
        },
        "author": {
            "type": "str",
            "default": ""
        },
        "venvs": {
            "type": "str",
            "default": ".venvs"
        },
        "version": {
            "type": "str",
            "default": ""
        },
        "main": {
            "type": "str",
            "default": "run.py"
        },
        "scripts": {
            "type": "dict",
            "default": {}
        },
        "url": {
            "type": "str",
        },
        "dependencies": {
            "type": "dict",
            "default": {}
        }
    }

    @property
    def dependencies(self) -> dict:
        return self.get("dependencies", {})

    def get_dependencies(self, name) -> str:
        return self.dependencies.get(name, None)

    def get_all_dependencies(self) -> list[str]:
        return [i for i in self.dependencies.keys()]