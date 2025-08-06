from vebp.install import Installer


def install_command(args, app):
    installer = Installer(app)

    packages = getattr(args, "packages", [])

    if not packages:
        installer.for_package()
        return

    installer.install(packages)