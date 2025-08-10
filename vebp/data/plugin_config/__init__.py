from vebp.data import BaseData


class PluginConfig(BaseData):
    FILENAME = "vebp-plugin.json"

    PROPERTY = {
        "define": {
            "chicken": {
                "func": {
                    "generate": True,
                    "default": "func"
                }
            }
        },
        "devDependencies": {
            "generate": True,
            "default": []
        }
    }