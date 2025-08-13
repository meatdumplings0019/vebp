from vebp.data import BaseData


class BuildConfig(BaseData):
    FILENAME = "vebp-build.json"

    PROPERTY = {
        "console": {
            "generate": True,
            "default": False,
        },
        "auto_run": {},
        "icon": {},
        "onefile": {},
        "assets": {},
        "in_assets": {},
        "sub_project": {},
        "exclude_modules": {},
        "exclude_commands": {},
        "before_events": {}
    }