import os
import sys
import tempfile
import uuid
from typing import List

from dict_tools import data


def __init__(hub):
    """
    :param hub: The redistributed pop central hub.
    """
    hub.pop.sub.load_subdirs(hub.tiamat)
    os.environ["POP_BUILD"] = "1"
    os.environ["TIAMAT_BUILD"] = "1"
    hub.tiamat.BUILDS = {}
    hub.tiamat.SYSTEMD = ("rhel7", "rhel8", "arch", "debian10")
    hub.tiamat.SYSTEMD_DIR = "usr/lib/systemd/system/"
    hub.tiamat.SYSV = ("rhel5", "rhel6")
    hub.tiamat.SYSV_DIR = "etc/init.d"


def cli(hub):
    """
    Execute the routine from the CLI.

    :param hub: The redistributed pop central hub.
    """
    hub.pop.config.load(["tiamat"], cli="tiamat")
    if hub.SUBPARSER == "build":
        hub.tiamat.build.builder(
            name=hub.OPT.tiamat.name,
            requirements=hub.OPT.tiamat.requirements,
            sys_site=hub.OPT.tiamat.system_site,
            exclude=hub.OPT.tiamat.exclude,
            directory=os.path.abspath(hub.OPT.tiamat.directory),
            pyinstaller_version=hub.OPT.tiamat.pyinstaller_version,
            pyinstaller_runtime_tmpdir=hub.OPT.tiamat.pyinstaller_runtime_tmpdir,
            datas=hub.OPT.tiamat.datas,
            build=hub.OPT.tiamat.build,
            pkg=hub.OPT.tiamat.pkg,
            onedir=hub.OPT.tiamat.onedir,
            pyenv=hub.OPT.tiamat.pyenv,
            run=hub.OPT.tiamat.run,
            no_clean=hub.OPT.tiamat.no_clean,
            locale_utf8=hub.OPT.tiamat.locale_utf8,
            dependencies=hub.OPT.tiamat.dependencies,
            release=hub.OPT.tiamat.release,
            pkg_tgt=hub.OPT.tiamat.pkg_tgt,
            pkg_builder=hub.OPT.tiamat.pkg_builder,
            srcdir=hub.OPT.tiamat.srcdir,
            system_copy_in=hub.OPT.tiamat.system_copy_in,
            tgt_version=hub.OPT.tiamat.tgt_version,
            venv_plugin=hub.OPT.tiamat.venv_plugin,
            python_bin=hub.OPT.tiamat.python_bin,
            omit=hub.OPT.tiamat.omit,
            pyinstaller_args=hub.OPT.tiamat.pyinstaller_args,
            timeout=hub.OPT.tiamat.timeout,
            pip_version=hub.OPT.tiamat.pip_version,
        )
    elif hub.SUBPARSER == "clean":
        hub.tiamat.clean.all(hub.OPT.tiamat.directory)
    elif hub.SUBPARSER == "install":
        raise NotImplementedError()
    elif hub.SUBPARSER == "freeze":
        if getattr(sys, "frozen", False):
            freeze = os.path.join(sys._MEIPASS, "app_freeze.txt")
            with open(freeze) as fh:
                print(fh.read())
        else:
            raise OSError("freeze can only be called when tiamat is run as a binary")
    elif hub.SUBPARSER is None:
        hub.config.ARGS["parser"].print_help()
        sys.exit()


def new(
    hub,
    name: str,
    requirements: str,
    sys_site: bool,
    exclude: List[str],
    directory: str,
    pyinstaller_version: str = "4.0",
    pyinstaller_runtime_tmpdir: str = None,
    datas: set = None,
    build: str = None,
    pkg: str = None,
    onedir: bool = False,
    pyenv: str = "system",
    run: str = "run.py",
    locale_utf8: bool = False,
    dependencies: str = None,
    release: str = None,
    pkg_tgt: str = None,
    pkg_builder: str = None,
    srcdir: str = None,
    system_copy_in: List[str] = None,
    python_bin: str = None,
    omit: List[str] = None,
    pyinstaller_args: List[str] = None,
    venv_plugin: str = None,
    timeout: int = 300,
    pip_version: str = "latest",
) -> str:
    """
    :param hub: The redistributed pop central hub.
    :param name: The name of the project to build.
    :param requirements: The name of the requirements.txt file to use.
    :param sys_site: Include the system site-packages when building.
    :param exclude: A list of exclude files or python modules, these python packages
        will be ignored by pyinstaller
    :param directory: The path to the directory to build from.
        This denotes the root of the python project source tree to work from.
        This directory should have the setup.py and the paths referenced in
        configurations will assume that this is the root path they are working from.
    :param pyinstaller_version: The version of pyinstaller to use for packaging
    :param pyinstaller_runtime_tmpdir: Pyinstaller runtime tmpdir.
    :param datas: PyInstaller datas mapping
    :param build: Enter in commands to build a non-python binary into the
        deployed binary.
        The build options are set on a named project basis. This allows for multiple
        shared binaries to be embedded into the final build:

        build:
          libsodium:
            make:
              - wget libsodium
              - tar xvf libsodium*
              - cd libsodium
              - ./configure
              - make
            src: libsodium/libsodium.so
            dest: lib64/
    :param pkg: Options for building packages.
    :param onedir: Instead of producing a single binary produce a directory with
        all components.
    :param pyenv: The python version to build with.
    :param run: The location of the project run.py file.
    :param locale_utf8: Use the UTF-8 locale with PyInstaller, as in PEP538 and PEP540.
    :param dependencies: Comma separated list of dependencies needed for the build.
    :param release: Release string i.e. '1.el7'.
    :param pkg_tgt: The os/distribution target to build the package against.
    :param pkg_builder: The package builder plugin to use.
    :param srcdir: Install all of the python package sources and/or wheels found in
        this directory.
    :param system_copy_in: A list of directories to copy into the build venv that are
        not otherwise detected.
    :param python_bin: The python binary to use for system calls
    :param omit: Omit files by glob
    :param pyinstaller_args: Args to pass straight through to pyinstaller
    :param venv_plugin: The virtualenvironment plugin to use
    :param timeout: The amount of time (seconds) before a command is considered to
        have failed
    :param pip_version: The version of pip to use while packaging
    :return: The build name.
    """
    if name == "." or name is None:
        name = os.path.basename(os.path.abspath("."))
    venv_dir = tempfile.mkdtemp()
    is_win = os.name == "nt"
    if python_bin is None:
        if is_win:
            python_bin = os.path.join(venv_dir, "Scripts", "python")
        else:
            python_bin = os.path.join(venv_dir, "bin", "python3")
    if is_win:
        s_path = os.path.join(venv_dir, "Scripts", name)
    elif locale_utf8:
        s_path = "env PYTHONUTF8=1 LANG=POSIX " + os.path.join(venv_dir, "bin", name)
    else:
        s_path = os.path.join(venv_dir, "bin", name)

    if datas is None:
        datas = set()

    cmd = [python_bin, "-B", "-OO", "-m", "PyInstaller"]

    # Determine the python modules that should be excluded
    excluded = set()
    for ex in exclude:
        if os.path.isfile(ex):
            with open(ex) as exf:
                for line in exf:
                    line = line.strip()
                    if line:
                        excluded.add(line)
        else:
            excluded.add(ex)

    for ex in excluded:
        cmd.extend(["--exclude-module", ex])

    bname = str(uuid.uuid1())
    requirements = os.path.join(directory, requirements)
    hub.tiamat.BUILDS[bname] = data.NamespaceDict(
        name=name,
        build=build,
        pkg=pkg,
        pkg_tgt=pkg_tgt,
        pkg_builder=pkg_builder,
        dependencies=dependencies,
        release=release,
        binaries=[],
        is_win=is_win,
        exclude=excluded,
        requirements=requirements,
        sys_site=sys_site,
        dir=os.path.abspath(directory),
        srcdir=srcdir,
        pyinstaller_version=pyinstaller_version,
        pyinstaller_runtime_tmpdir=pyinstaller_runtime_tmpdir,
        system_copy_in=system_copy_in,
        run=os.path.join(directory, run),
        spec=os.path.join(directory, f"{name}.spec"),
        pybin=python_bin,
        s_path=s_path,
        venv_dir=venv_dir,
        vroot=os.path.join(venv_dir, "lib"),
        onedir=onedir,
        all_paths=set(),
        imports=set(),
        datas=datas,
        cmd=cmd,
        pyenv=pyenv,
        pypi_args=[
            s_path,
            "--log-level=INFO",
            "--noconfirm",
            "--onedir" if onedir else "--onefile",
            "--clean",
        ]
        + list(pyinstaller_args),
        locale_utf8=locale_utf8,
        omit=omit,
        venv_plugin=venv_plugin,
        timeout=timeout,
        pip_version=pip_version,
    )
    req = hub.tiamat.build.mk_requirements(bname)
    hub.tiamat.BUILDS[bname].req = req
    return bname
