"""
Create and manage the venvs used for build environments.
"""
import os
from typing import List

__func_alias__ = {"bin_": "bin"}


def bin_(hub, bname: str) -> List[str]:
    """
    Ensure that the desired binary version is present and return the path to
    the python bin to call.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    root = hub.tiamat.cmd.run(["pyenv", "root"], fail_on_error=True).stdout.strip()

    avail = set()
    for line in root.split("\n"):
        avail.add(line.strip())

    python_env = hub.tiamat.virtualenv.init.env(bname)
    if opts.pyenv not in avail:
        if "env" not in python_env:
            python_env.append("env")
        hub.tiamat.cmd.run(
            python_env
            + [
                'PYTHON_CONFIGURE_OPTS="--enable-shared --enable-ipv6"',
                'CONFIGURE_OPTS="--enable-shared --enable-ipv6"',
                "pyenv",
                "install",
                opts.pyenv,
            ],
            fail_on_error=True,
        )
    return python_env + [os.path.join(root, "versions", opts.pyenv, "bin", "python3")]


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    env_bin = hub.tiamat.virtualenv.pyenv.bin(bname)
    cmd = env_bin + [opts.venv_dir, "--clear"]
    if opts.sys_site:
        cmd.append("--system-site-packages")
    hub.tiamat.cmd.run(cmd, fail_on_error=True)
