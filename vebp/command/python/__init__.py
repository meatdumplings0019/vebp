from vebp.utils import print_python


def python_command(args, app):
    if getattr(args, "version", False):
        print_python(app.python_version)