def plugin_get_assets_path(app, namespace):
    return app.plugin_manager.get_plugin(namespace).assets
