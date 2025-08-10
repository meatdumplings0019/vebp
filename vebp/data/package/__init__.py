from vebp.data import BaseData


class Package(BaseData):
    FILENAME = "vebp-package.json"

    PROPERTY = {
        "name": {
            "type": "str",
            "generate": True,
            "default": "$name"
        },
        "author": {
            "type": "str",
            "generate": True,
            "default": ""
        },
        "venv": {
            "type": "str",
            "generate": True,
            "default": ".venv"
        },
        "version": {
            "type": "str",
            "generate": True,
            "default": ""
        },
        "main": {
            "type": "str",
            "generate": True,
            "default": "run.py"
        },
        "scripts": {
            "type": "dict",
            "generate": True,
            "default": {}
        },
        "url": {
            "type": "str",
        },
        "dependencies": {
            "type": "dict",
            "generate": True,
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