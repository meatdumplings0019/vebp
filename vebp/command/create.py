from vebp.create import Create


def create_command(args, app):
    name = getattr(args, "name", None)

    obj = Create(app)
    obj.start(name)