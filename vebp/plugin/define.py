def plugin_get_assets_path(app, namespace):
    return app.plugin_manager.get_plugin(namespace).assets

def plugin_get_data_path(app, namespace):
    return app.plugin_manager.get_plugin(namespace).data