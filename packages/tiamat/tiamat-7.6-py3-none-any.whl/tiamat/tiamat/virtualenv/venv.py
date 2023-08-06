from typing import List


__func_alias__ = {"bin_": "bin"}


def env(hub, bname) -> List[str]:
    python_env = hub.tiamat.virtualenv.init.env(bname)
    if "env" not in python_env:
        python_env.append("env")
    return python_env + [
        'PYTHON_CONFIGURE_OPTS="--enable-shared --enable-ipv6"',
        'CONFIGURE_OPTS="--enable-shared --enable-ipv6"',
    ]


def bin_(hub, bname: str) -> List[str]:
    """
    Ensure that the desired binary version is present and return the path to
    the python bin to call.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    ret = hub.tiamat.cmd.run(["which", "venv"]).stdout.rstrip()
    if ret:
        venv_bin = [ret]
    else:
        venv_bin = [opts.pybin, "-m", "venv"]

    hub.tiamat.cmd.run(venv_bin + ["--help"], fail_on_error=True)
    return venv_bin


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]

    cmd = (
        hub.tiamat.virtualenv.venv.env(bname)
        + hub.tiamat.virtualenv.venv.bin(bname)
        + [opts.venv_dir, "--clear"]
    )
    if opts.sys_site:
        cmd.append("--system-site-packages")

    hub.tiamat.cmd.run(cmd, fail_on_error=True)
