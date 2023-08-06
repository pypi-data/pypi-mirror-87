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
    ret = hub.tiamat.cmd.run(["which", "virtualenv"]).stdout.rstrip()
    if ret:
        virtualenv_bin = [ret]
    else:
        virtualenv_bin = [opts.pybin, "-m", "virtualenv", "--verbose"]

    hub.tiamat.cmd.run(
        virtualenv_bin + ["--help"], timeout=opts.timeout, fail_on_error=True
    )

    return virtualenv_bin


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]

    env_bin = hub.tiamat.virtualenv.virtualenv.bin(bname)
    cmd = env_bin + [opts.venv_dir, "--clear"]
    pyenv = opts.get("pyenv")
    if pyenv and pyenv != "system":
        cmd.extend(["--python", opts.pyenv])
    if opts.sys_site:
        cmd.append("--system-site-packages")

    hub.tiamat.cmd.run(cmd, timeout=opts.timeout, fail_on_error=True)
