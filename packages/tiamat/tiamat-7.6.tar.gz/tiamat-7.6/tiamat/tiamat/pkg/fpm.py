import os
import shutil
import tempfile
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set


def build(hub, bname: str):
    """
    Build a new package using fpm.

    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    root = os.path.join(tempfile.mkdtemp(), opts.name)
    os.makedirs(root)
    # Move files into a tempdir, return config files
    # Set the specific flags, like checksum type, based on the pkg_tgt
    # Run fpm
    config = _prep_tmpdir(
        hub,
        opts.name,
        root,
        opts.pkg,
        opts.pkg_tgt,
        opts.dir,
        opts.onedir,
    )
    cmd = _get_cmd(
        opts.name,
        root,
        opts.dependencies,
        opts.release,
        opts.pkg,
        opts.pkg_tgt,
        opts.version,
        config,
    )
    hub.tiamat.cmd.run(cmd, fail_on_error=True)
    # shutil.rmtree(root)


def _get_fpm_tgt(pkg_tgt: str):
    """
    Turn the pkg_tgt into a target for fpm.

    :param pkg_tgt: The os/distribution target to build the package against.
    """
    rpm = (
        "rpm",
        "fedora",
        "redhat",
        "rhel",
        "opensuse",
        "suse",
        "cent",
        "centos",
        "sles",
        "sle",
    )
    deb = ("ubuntu", "deb")
    pacman = ("arch", "manjaro", "pacman")
    if pkg_tgt.lower().startswith(rpm):
        return "rpm"
    elif pkg_tgt.startswith(deb):
        return "deb"
    elif pkg_tgt.lower().startswith(pacman):
        return "pacman"
    else:
        raise ValueError(f"invalid pkg target: {pkg_tgt}")


def _get_cmd(
    name: str,
    root: str,
    dependencies: Iterable[str],
    release: str,
    pkg: Dict[str, str],
    pkg_tgt: str,
    version: str,
    config: Iterable[str],
) -> List[str]:
    """
    Return the command line args list to shell out to fpm with.

    :param name: The name of the project to build.
    :param root: The path to the directory to build from.
    :param dependencies: comma separated list of dependencies needed for the build.
    :param release: This is the fpm --iteration option i.e. "1.el7".
    :param pkg: Options for building packages.
    :param pkg_tgt: The os/distribution target to build the package against.
    :param version: Target package version.
    :param config: Load extra options from a configuration file.
    """
    version = str(pkg.get("version", version))
    fpm_tgt = _get_fpm_tgt(pkg_tgt)
    fpm = shutil.which("fpm")
    if not fpm:
        raise OSError("fpm command is not available")
    cmd = [fpm, "-s", "dir", "-n", name, "-t", fpm_tgt]

    for fn in sorted(list(config)):
        cmd.append("--config-files")
        cmd.append(fn)
    if fpm_tgt == "rpm":
        cmd.append("--rpm-digest")
        cmd.append("sha512")
    if dependencies:
        for dependency in dependencies:
            cmd.append("-d")
            cmd.append(f"{dependency}")
    if release:
        cmd.append("--iteration")
        cmd.append(f"{release}")
    if pkg.get("after-install"):
        cmd.append("--after-install")
        cmd.append(pkg.get("after-install"))
    if pkg.get("before-install"):
        cmd.append("--before-install")
        cmd.append(pkg.get("before-install"))
    if pkg.get("after-remove"):
        cmd.append("--after-remove")
        cmd.append(pkg.get("after-remove"))
    if pkg.get("before-remove"):
        cmd.append("--before-remove")
        cmd.append(pkg.get("before-remove"))
    if pkg.get("after-upgrade"):
        cmd.append("--after-upgrade")
        cmd.append(pkg.get("after-upgrade"))
    if pkg.get("before-upgrade"):
        cmd.append("--before-upgrade")
        cmd.append(pkg.get("before-upgrade"))
    cmd.append("--version")
    cmd.append(version)
    cmd.append("-C")
    cmd.append(root)
    return cmd


def _prep_tmpdir(
    hub,
    name: str,
    root: str,
    pkg: Dict[str, str],
    pkg_tgt: str,
    dir_: str,
    onedir: bool,
) -> Set[str]:
    """
    Make the tempdir and copy the configured files into it.

    :param hub:
    :param name:
    :param root:
    :param pkg:
    :param pkg_tgt:
    :param dir_:
    :param onedir:
    :return:
    """
    script_template = """#!/bin/sh
    {bin_path} $@"""
    dist = os.path.join(dir_, "dist", name)
    configs = set()
    bin_tgt = os.path.join(root, "usr", "bin")
    if onedir:
        dist = os.path.join(dir_, "dist", "run")
        tree_tgt = os.path.join(root, "opt", "run", "bins")
        pbin = os.path.join(f"{os.sep}opt", "run", "bins", "run")
        os.makedirs(os.path.dirname(tree_tgt))
        shutil.copytree(dist, tree_tgt)
        os.makedirs(bin_tgt)
        script_output = script_template.format(bin_path=pbin)
        with open(os.path.join(bin_tgt, name), "w") as script_file:
            script_file.write(script_output)
        os.chmod(os.path.join(bin_tgt, name), 0o755)
    else:
        os.makedirs(bin_tgt)
        shutil.copy(dist, bin_tgt)
    for tpath, spath in pkg.get("config", {}).items():
        tpath = tpath.strip(os.sep)
        src = os.path.join(dir_, spath)
        tgt = os.path.join(root, tpath)
        tgt_dir = os.path.dirname(tgt)
        if not os.path.isdir(tgt_dir):
            os.makedirs(tgt_dir)
        shutil.copy(src, tgt)
        configs.add(tpath)
    for spath in pkg.get("scripts", {}):
        src = os.path.join(dir_, spath)
        if not os.path.isdir(bin_tgt):
            os.makedirs(bin_tgt)
        shutil.copy(src, bin_tgt)
    if pkg_tgt in hub.tiamat.SYSTEMD:
        tgt = os.path.join(root, hub.tiamat.SYSTEMD_DIR)
        for spath in pkg.get("systemd", {}):
            if not os.path.isdir(tgt):
                os.makedirs(tgt)
            src = os.path.join(dir_, spath)
            shutil.copy(src, tgt)
    if pkg_tgt in hub.tiamat.SYSV:
        tgt = os.path.join(root, hub.tiamat.SYSV_DIR)
        for spath in pkg.get("sysv", {}):
            if not os.path.isdir(tgt):
                os.makedirs(tgt)
            src = os.path.join(dir_, spath)
            shutil.copy(src, tgt)
    return configs
