from vebp.builder.plugin import PluginBuilder


def plugin_build_command(args, app):
    pb = PluginBuilder(getattr(args, "path", None))
    pb.build()