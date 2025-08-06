from vebp.install import Installer


def uninstall_command(args, app):
    installer = Installer(app)

    packages = getattr(args, "packages", [])

    if not packages:
        print(f"你要卸载什么?")
        return

    installer.uninstall(packages)