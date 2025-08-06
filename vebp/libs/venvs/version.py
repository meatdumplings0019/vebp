from importlib.metadata import version

def get_package_version(pkg):
    return version(pkg.split("==")[0])
