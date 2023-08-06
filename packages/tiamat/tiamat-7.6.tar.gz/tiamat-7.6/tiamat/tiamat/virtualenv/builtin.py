import os
import shutil
import sys
import venv
from typing import List

__func_alias__ = {"bin_": "bin"}


def bin_(hub, bname: str) -> List[str]:
    """

    :param hub:
    :param bname:
    :return:
    """
    opts = hub.tiamat.BUILDS[bname]
    if os.path.isfile(opts.pybin):
        return [opts.pybin]
    elif getattr(sys, "frozen", False):
        # If sys.frozen is set, then we are running in a tiamat binary
        hub.log.debug("Running inside a binary, searching for system python")
        return [shutil.which("python3")]
    else:
        hub.log.debug("Using system executable to build virtualenv")
        return [sys.executable]


def create(hub, bname: str):
    """
    Change up the opts for this build so that they use the appropriate system python
    directories

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    pybin = hub.tiamat.virtualenv.builtin.bin(bname)

    if hasattr(sys, "frozen"):
        # some venv functions need to be overriden if we are running from a tiamat
        # binary
        sys._base_executable = pybin[0]

    builder = venv.EnvBuilder(
        system_site_packages=opts.sys_site,
        clear=True,
        symlinks=False,
        upgrade=True,
        with_pip=True,
        prompt=None,
    )
    builder.create(opts.venv_dir)

    # Reset sys base executable
    if hasattr(sys, "frozen"):
        sys._base_executable = sys.executable
