from vebp.data import BaseData


class PluginConfig(BaseData):
    FILENAME = "vebp-plugin.json"

    PROPERTY = {
        "define": {
            "chicken": {
                "func": {
                    "default": "func"
                }
            }
        }
    }