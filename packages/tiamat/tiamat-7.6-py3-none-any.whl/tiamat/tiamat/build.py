"""
The build plugin is used to execute the build routines for non-python components.
"""
import glob
import os
import pprint
import shutil
import tempfile
from typing import List

import requests


def mk_requirements(hub, bname: str) -> str:
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    :return:
    """
    opts = hub.tiamat.BUILDS[bname]
    req = os.path.join(opts.dir, "__build_requirements.txt")
    with open(opts.requirements) as rfh:
        data_ = rfh.read()
    with open(req, "w+") as wfh:
        wfh.write(data_)
    return req


def builder(
    hub,
    name,
    requirements: str,
    sys_site: str,
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
    no_clean: bool = False,
    locale_utf8: bool = False,
    dependencies: str = None,
    release: str = None,
    pkg_tgt: str = None,
    pkg_builder: str = None,
    srcdir: str = None,
    system_copy_in: List[str] = None,
    tgt_version: str = None,
    python_bin: str = None,
    omit: List[str] = None,
    venv_plugin: str = None,
    pyinstaller_args: List[str] = None,
    timeout: int = 300,
    pip_version: str = "latest",
):
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
    :param build: Enter in commands to build a non-python binary into the deployed
        binary.
        The build options are set on a named project basis. This allows for multiple
        shared binaries to be embedded into the final build:

    .. code-block:: yaml

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
    :param no_clean: Don't run the clean up sequence, this will leave the venv, spec
        file and other artifacts.
    :param locale_utf8: Use the UTF-8 locale with PyInstaller, as in PEP538 and PEP540.
    :param dependencies: Comma separated list of dependencies needed for the build.
    :param release: Release string i.e. '1.el7'.
    :param pkg_tgt: The os/distribution target to build the package against.
    :param pkg_builder: The package builder plugin to use.
    :param srcdir: Install all of the python package sources and/or wheels found in
        this directory.
    :param system_copy_in: A list of directories to copy into the build venv that are
        not otherwise detected.
    :param tgt_version: Target package version.
    :param python_bin: The python binary to use for system calls
    :param pyinstaller_args: Args to pass straight through to pyinstaller
    :param venv_plugin: The virtual environment plugin to use
    :param timeout: The amount of time (seconds) before a command is considered to
        have failed
    :param pip_version: The version of pip to use while packaging
    """

    bname = hub.tiamat.init.new(
        name=name,
        requirements=requirements,
        sys_site=sys_site,
        exclude=exclude or [],
        directory=directory,
        pyinstaller_version=pyinstaller_version,
        pyinstaller_runtime_tmpdir=pyinstaller_runtime_tmpdir,
        datas=datas,
        build=build,
        pkg=pkg,
        onedir=onedir,
        pyenv=pyenv,
        run=run,
        locale_utf8=locale_utf8,
        dependencies=dependencies,
        release=release,
        pkg_tgt=pkg_tgt,
        pkg_builder=pkg_builder,
        srcdir=srcdir,
        system_copy_in=system_copy_in,
        python_bin=python_bin,
        omit=omit,
        pyinstaller_args=pyinstaller_args or [],
        venv_plugin=venv_plugin,
        timeout=timeout,
        pip_version=pip_version,
    )
    hub.log.debug(
        f"Build config '{bname}':\n{pprint.pformat(hub.tiamat.BUILDS[bname])}"
    )
    hub.tiamat.virtualenv.init.create(bname)
    if tgt_version:
        hub.tiamat.BUILDS[bname].version = tgt_version
    else:
        hub.tiamat.data.version(bname)
    hub.tiamat.build.make(bname)
    hub.tiamat.virtualenv.init.scan(bname)
    hub.tiamat.virtualenv.init.mk_adds(bname)
    hub.tiamat.inst.mk_spec(bname)
    hub.tiamat.inst.call(bname)
    if pkg_tgt:
        hub.tiamat.pkg.init.build(bname)
    hub.tiamat.post.report(bname)
    if not no_clean:
        hub.tiamat.post.clean(bname)


def make(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    build = opts.build
    if not build:
        return
    bdir = tempfile.mkdtemp()
    cur_dir = os.getcwd()
    os.chdir(bdir)
    if opts.srcdir:
        for fn in os.listdir(opts.srcdir):
            shutil.copy(os.path.join(opts.srcdir, fn), bdir)
    for proj, conf in build.items():
        if not opts.srcdir:
            if "sources" in conf:
                sources = conf["sources"]
                if isinstance(sources, str):
                    sources = [sources]
                for source in sources:
                    response = requests.get(source)
                    with open(
                        os.path.join(bdir, os.path.split(source)[1]), "wb"
                    ) as file:
                        file.write(response.content)
        if "make" in conf:
            for cmd in conf["make"]:
                hub.tiamat.cmd.run(
                    cmd, shell=True, cwd=bdir, timeout=opts.timeout, fail_on_error=True
                )
        if "src" in conf and "dest" in conf:
            srcs = conf["src"]
            dest = os.path.join(opts.venv_dir, conf["dest"])
            hub.log.info(f"Copying: {srcs}->{dest}")
            if not isinstance(srcs, (list, tuple)):
                srcs = [srcs]
            final_srcs = set()
            for src in srcs:
                globed = glob.glob(src)
                if not globed:
                    hub.log.warning(f"Expression f{src} does not match any file paths")
                    continue
                final_srcs.update(globed)
            for src in final_srcs:
                fsrc = os.path.join(bdir, src)
                if os.path.isfile(fsrc):
                    try:
                        shutil.copy(fsrc, dest, follow_symlinks=True)
                    except OSError as e:
                        hub.log.warning(f"Unable to copy file {fsrc} to {dest}: {e}")
                    hub.tiamat.BUILDS[bname].binaries.append(
                        (os.path.join(dest, os.path.basename(fsrc)), ".")
                    )
                elif os.path.isdir(fsrc):
                    shutil.copytree(fsrc, dest)
                else:
                    hub.log.warning(f"FAILED TO FIND FILE {fsrc}")
    os.chdir(cur_dir)
