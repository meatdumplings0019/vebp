def plugin_uninstall_command(args, app):
    app.plugin_manager.uninstall(getattr(args, "name", None))