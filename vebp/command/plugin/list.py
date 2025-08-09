def plugin_list_command(args, app):
    lst = app.plugin_manager.get_all_plugins()
    if not lst:
        print(f"未安装插插件")
        return

    for plugin in lst:
        print(f"插件名称: {plugin.namespace}")
        print(f"作者: {plugin.author}")
        print(f"启用: {"✅" if plugin.action else "❌"}")
        print()