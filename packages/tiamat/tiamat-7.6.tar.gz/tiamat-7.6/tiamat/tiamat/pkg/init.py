def build(hub, bname: str):
    """
    Given the build arguments, Make a package!

    :param bname: The name of the build configuration to use from the build.conf file.
    """
    pkg_builder = hub.OPT.tiamat.pkg_builder
    build_func = getattr(hub.tiamat.pkg, pkg_builder).build
    build_func(bname)
