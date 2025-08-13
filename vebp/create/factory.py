from vebp.create.obj import CreateObject


def create_object_factory_function(name, func, data):
    return CreateObject(name, func, data)