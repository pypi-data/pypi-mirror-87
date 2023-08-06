import os
import shlex
import subprocess
import sys
from typing import Any
from typing import Dict
from typing import List

from dict_tools import data

__virtualname__ = "cmd"


def run(
    hub,
    cmd: List[str] or str,
    shell: bool = False,
    env: Dict[str, str] = None,
    cwd: str = None,
    timeout: int = 300,
    fail_on_error: bool = False,
    **kwargs,
) -> Dict[str, Any]:
    """
    Run every command the same way
    :param hub:
    :param cmd:
    :param shell:
    :param env:
    :param cwd:
    :param timeout:
    :param fail_on_error:
    :return:
    """
    if env is None and getattr(sys, "frozen", False):
        env = os.environ.copy()
        # Remove the LOAD LIBRARY_PATH for running commands
        # https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#ld-library-path-libpath-considerations
        env.pop("DYLD_LIBRARY_PATH", None)  # Darwin
        env.pop("LD_LIBRARY_PATH", None)  # Linux
        env.pop("LIBPATH", None)  # AIX

    if cwd is None:
        cwd = os.getcwd()

    if shell is True:
        if isinstance(cmd, str):
            cmd = " ".join(c for c in shlex.split(cmd))
        else:
            cmd = " ".join(shlex.quote(c) for c in cmd)
    elif isinstance(cmd, str):
        cmd = cmd.split()

    dry_run = hub.OPT.tiamat.dry_run
    if dry_run:
        hub.log.debug(f"Dry run command: {cmd}")
        return data.NamespaceDict(
            retcode=0, stdout="()", stderr=f"Dry Run: {cmd}", dry_run=dry_run
        )

    hub.log.info(f"Running {cmd} in {cwd} ...")

    proc = subprocess.run(
        cmd,
        shell=shell,
        timeout=timeout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=env,
        cwd=cwd,
        **kwargs,
    )
    message = (
        f"Command {cmd} running in {cwd} completed.\n"
        f" Dry-Run: {dry_run}\n"
        f" Exitcode: {proc.returncode}\n"
    )
    if proc.stdout or proc.stderr:
        message += " Process Output:\n"
    if proc.stdout:
        message += f"   >>>>> STDOUT >>>>>\n{proc.stdout}\n   <<<<< STDOUT <<<<<\n"
    if proc.stderr:
        message += f"   >>>>> STDERR >>>>>\n{proc.stderr}\n   <<<<< STDERR <<<<<\n"

    if proc.returncode != 0:
        hub.log.error(message)
    else:
        hub.log.debug(message)

    if fail_on_error:
        proc.check_returncode()

    return data.NamespaceDict(
        retcode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        dry_run=False,
    )
