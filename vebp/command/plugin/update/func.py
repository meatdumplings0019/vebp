from vebp.plugin.utils import copy_func_file


def plugin_update_func_command(args, app):
    copy_func_file(app, args.path)