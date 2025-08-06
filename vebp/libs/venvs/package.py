from importlib.metadata import version


def is_package_installed(pkg):
    try:
        name = pkg.split('==')[0]
        version(name)
        return True
    except ImportError:
        return False
