__func_alias__ = {"bin_": "bin"}


def bin_(hub, bname: str) -> str:
    """
    Ensure that the desired binary version is present and return the path to
    the python bin to call.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    pyvenv_bin = hub.tiamat.cmd.run(["which", "pyvenv"]).stdout.rstrip()
    hub.tiamat.cmd.run([pyvenv_bin, "--help"], fail_on_error=True)
    return pyvenv_bin


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]

    env_bin = hub.tiamat.virtualenv.pyvenv.bin(bname)
    cmd = [env_bin, opts.venv_dir, "--clear"]
    if opts.sys_site:
        cmd.append("--system-site-packages")

    hub.tiamat.cmd.run(cmd, fail_on_error=True)
