def plugin_unload_command(args, app):
    app.plugin_manager.unload_plugin(getattr(args, "name", None))