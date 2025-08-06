def plugin_install_command(args, app):
    app.plugin_manager.install(getattr(args, "path", None))