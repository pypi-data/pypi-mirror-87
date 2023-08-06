import ast
import fnmatch
import os
import re
import shutil
import tarfile
from typing import Dict
from typing import List
from typing import Set

# "venv" is a keyword for bash, call the directory "virtualenv" but allow it to be
# accessed with the alias
__sub_alias__ = ["venv"]
__func_alias__ = {"bin_": "bin"}

OMIT = (
    "__pycache__",
    "PyInstaller",
)


def bin_(hub, bname: str) -> List[str]:
    func = getattr(hub.tiamat.virtualenv, hub.OPT.tiamat.venv_plugin).bin
    return func(bname)


def freeze(hub, bname: str) -> Set[str]:
    """
    List the requirements inside the given virtual environment sans those excluded by
    the build

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]

    # Freeze the modules installed into the environment
    ret = hub.tiamat.cmd.run(
        [opts.pybin, "-m", "pip", "freeze", "--all", "--exclude-editable"],
        cwd=opts.srcdir,
        timeout=opts.timeout,
        fail_on_error=True,
    )

    standardize_name = (
        lambda item: re.split("[= ]", item, maxsplit=1)[0].lower().replace("_", "-")
    )

    # Compare apples to apples, remove everything after "==" or " " from the excludes
    # and the freeze
    excluded = {standardize_name(ex) for ex in opts.exclude}

    bundled_modules = set()
    for module in ret.stdout.splitlines():
        if standardize_name(module) not in excluded:
            bundled_modules.add(module)

    return bundled_modules


def create(hub, bname: str):
    """
    Make a virtual environment based on the version of python used to call this script.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    func = getattr(hub.tiamat.virtualenv, opts.venv_plugin).create
    hub.log.debug(f"Creating virtual environment with {opts.venv_plugin}")
    func(bname)

    return hub.tiamat.virtualenv.init.setup_pip(bname)


def env(hub, bname) -> List[str]:
    opts = hub.tiamat.BUILDS[bname]
    ret = []
    if opts.locale_utf8:
        ret.extend(["env", "PYTHONUTF8=1", "LANG=POSIX"])
    return ret


def scan(hub, bname: str):
    """
    Scan the new venv for files and imports.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    omit = opts.omit or []
    for root, dirs, files in os.walk(opts.vroot):
        if _omit(root, omit):
            hub.log.trace(f"Ignoring root in {root}")
            continue
        for d in dirs:
            full = os.path.join(root, d)
            if _omit(full, omit):
                hub.log.trace(f"Ignoring dirs in {full}")
                continue
            opts.all_paths.add(full)
        for f in files:
            full = os.path.join(root, f)
            if _omit(full, omit):
                hub.log.trace(f"Ignoring full in {full}")
                continue
            opts.all_paths.add(full)


def mk_adds(hub, bname: str):
    """
    Make the imports and datas for PyInstaller.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    for path in opts.all_paths:
        if "site-packages" not in path:
            continue
        if os.path.isfile(path):
            if not path.endswith(".py"):
                continue
            if path.endswith("__init__.py"):
                # Skip it, we will get the dir
                continue
            imp = _to_import(path)
            if imp:
                opts.imports.add(imp)
        if os.path.isdir(path):
            data = _to_data(path)
            imp = _to_import(path)
            if imp:
                opts.imports.add(imp)
            if data:
                opts.datas.add(data)


def setup_pip(hub, bname: str):
    """
    Initialize pip in the new virtual environment

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    pip_cmd = [opts.pybin, "-m", "pip"]

    # Verify that an executable version of pip exists
    hub.tiamat.cmd.run(
        pip_cmd + ["--version"], timeout=opts.timeout, fail_on_error=True
    )

    if "latest" == opts.pip_version:
        pip_selection = "pip"
    else:
        pip_selection = f"pip=={opts.pip_version}"

    # Upgrade pip, setuptools, and wheel
    # Install old pycparser to fix: https://github.com/eliben/pycparser/issues/291
    pre_reqs = [
        pip_selection,
        "pyinstaller-hooks-contrib",
        "setuptools>=50.3.0",
        "wheel",
        "pycparser==2.14",
    ]

    version_str = hub.tiamat.cmd.run(
        [opts["pybin"], "-c", "import sys;print(tuple(sys.version_info))"],
        shell=True,
        timeout=opts.timeout,
        fail_on_error=True,
    ).stdout
    assert version_str, "Unable to determine target python version"

    version_info = ast.literal_eval(version_str)

    # distro is needed for Python3.8 and later. It replaces
    # platform.linux_distribution, which was included in Python until Python3.7
    if version_info >= (3, 8):
        pre_reqs.append("distro")

    # Install pre-requirements
    hub.tiamat.cmd.run(
        pip_cmd + ["install", "--upgrade"] + pre_reqs,
        timeout=opts.timeout,
        fail_on_error=True,
    )

    requirements = []
    if opts.get("req"):
        requirements.extend(["-r", opts.req])
    if opts.srcdir:
        files = _get_srcdir_files(opts.srcdir)
        requirements.extend(files)
    if os.path.isfile(os.path.join(opts.dir, "setup.py")):
        requirements.append(opts.dir)

    if ":" in opts.pyinstaller_version:
        pyinstall_version, pyinstall_path = opts.pyinstaller_version.split(":")
    else:
        pyinstall_version = opts.pyinstaller_version
        pyinstall_path = None

    if pyinstall_version == "dev":
        # Install development version of pyinstaller to run on python 3.8
        requirements.append(
            "https://github.com/pyinstaller/pyinstaller/tarball/develop"
        )
    elif pyinstall_version == "local":
        requirements.append("".join(pyinstall_path))
    else:
        requirements.append(f"PyInstaller=={pyinstall_version}")

    hub.tiamat.cmd.run(
        pip_cmd + ["install"] + requirements,
        cwd=opts.srcdir,
        timeout=opts.timeout,
        fail_on_error=True,
    )

    if opts.system_copy_in:
        _copy_in(hub, opts)

    ld_library_path = os.environ.get("LD_LIBRARY_PATH")
    venv_lib = os.path.join(opts.venv_dir, "lib")
    os.environ["LD_LIBRARY_PATH"] = f"{ld_library_path}:{venv_lib}".strip(":")
    # Add libpath to the environment for AIX
    os.environ[
        "LIBPATH"
    ] = f"{os.environ.get('LIBPATH')}:{os.path.join(opts.venv_dir, 'lib')}".strip(":")


def _omit(test: str, exlcude_patterns: List[str]) -> bool:
    """
    Check if a file should be omitted based on globs
    :param test: The string to compare to omit patterns
    :param exlcude_patterns: A glob to check against
    :return: True if the file should be omitted, else false
    """
    for bad in OMIT:
        if bad in test:
            return True

    return any(fnmatch.fnmatch(test, pattern) for pattern in exlcude_patterns)


def _to_import(path: str) -> str:
    """
    :param path:
    :return:
    """
    ret = path[path.index("site-packages") + 14 :].replace(os.sep, ".")
    if ret.endswith(".py"):
        ret = ret[:-3]
    return ret


def _to_data(path: str) -> str:
    """
    :param path:
    :return:
    """
    dest = path[path.index("site-packages") + 14 :]
    src = path
    if not dest.strip():
        return ""
    ret = f"{src}{os.pathsep}{dest}"
    return ret


def _copy_in(hub, opts: Dict[str, str]):
    """
    Copy in any extra directories from the python install.

    :param opts:
    """
    cmd = [opts["pybin"], "-c", "import sys;print(sys.path)"]
    tgt = ""
    dtgt = os.path.join(os.path.join(opts["venv_dir"], "lib"))
    for fn in os.listdir(dtgt):
        tmptgt = os.path.join(dtgt, fn)
        if os.path.isdir(tmptgt):
            tgt = os.path.join(tmptgt, "site-packages")

    data = hub.tiamat.cmd.run(
        cmd, shell=True, timeout=opts.timeout, fail_on_error=True
    ).stdout
    done = set()
    for path in ast.literal_eval(data):
        if not path:
            continue
        if not os.path.isdir(path):
            continue
        for fn in os.listdir(path):
            if fn in done:
                continue
            if fn in opts["system_copy_in"]:
                full = os.path.join(path, fn)
                if os.path.isdir(full):
                    shutil.copytree(full, os.path.join(tgt, fn))
                    done.add(fn)


def _get_srcdir_files(srcdir: str) -> List[str]:
    """
    Return the files that are python archives.

    :param srcdir:
    """
    files = []
    for fn in os.listdir(srcdir):
        if fn.endswith(".whl"):
            files.append(fn)
        if fn.endswith(".tar.gz"):
            # Might be a source archive
            with tarfile.open(fn) as tfp:
                for name in tfp.getnames():
                    if name.count(os.sep) > 1:
                        continue
                    if os.path.basename(name) == "PKG-INFO":
                        files.append(fn)
                        break
    return files
