from vebp.create.factory import create_object_factory_function
from vebp.create.obj import CreateObject


class Create:
    def __init__(self, app):
        self.app = app

        self.registry = {}

    def register(self):
        lst = self.app.plugin_manager.register_all("create", create_object_factory_function)
        for r in lst:
            for i in r.get():
                if isinstance(i, CreateObject):
                    self.registry[i.name] = i

    def start(self, name):
        self.register()
        item: CreateObject = self.registry.get(name, None)
        if item is None:
            raise KeyError(f"{name}不存在!")

        item.start()