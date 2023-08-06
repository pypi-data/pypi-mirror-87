"""
Use the system python interpreter and don't create an environment
"""
import os
import sys
from typing import List

__func_alias__ = {"bin_": "bin"}


def bin_(hub, bname: str) -> List[str]:
    """

    :param hub:
    :param bname:
    :return:
    """
    opts = hub.tiamat.BUILDS[bname]
    return opts.pybin or sys.executable


def create(hub, bname: str):
    """
    Change up the opts for this build so that they use the appropriate system python
    directories

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    pybin = hub.tiamat.virtualenv.system.bin(bname)

    # Prepare "virtual" environment by symlinking real binaries to that env
    bin_path = os.path.join(opts.venv_dir, "bin")
    os.makedirs(bin_path, exist_ok=True)
    python_path = os.path.join(bin_path, "python")
    python3_path = os.path.join(bin_path, "python3")

    # Symlink the environments pybin with the virtual environment
    os.symlink(pybin, python_path)
    os.symlink(pybin, python3_path)
