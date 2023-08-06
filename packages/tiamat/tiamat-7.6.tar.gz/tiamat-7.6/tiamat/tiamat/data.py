import os


def version(hub, bname: str):
    """
    Gather the version number of the pop project if possible.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    dir_ = hub.tiamat.BUILDS[bname].dir
    name = hub.tiamat.BUILDS[bname].name
    name = name.replace("-", "_")
    path = os.path.join(dir_, name, "version.py")
    _locals = {}
    version_ = "1"
    try:
        if os.path.isfile(path):
            with open(path) as fp:
                exec(fp.read(), None, _locals)
                version_ = _locals["version"]
    except Exception:
        pass
    hub.tiamat.BUILDS[bname].version = version_
