"""
Routines to manage the setup and invocation of pyinstaller.
"""
import os
import shutil


SPEC = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis([r"{s_path}"],
             pathex=[r"{cwd}"],
             binaries={binaries},
             datas={datas},
             hiddenimports={imports},
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
"""

SPEC_EXE = """

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=r"{name}",
          exclude_binaries={onedir},
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir={runtime_tmpdir},
          console=True )
"""

SPEC_COLL = """

exe = EXE(pyz,
          a.scripts,
          [],
          name=r"{name}",
          exclude_binaries={onedir},
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir={runtime_tmpdir},
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name=r"{name}")
"""


def mk_spec(hub, bname: str):
    """
    Create a spec file to build from.

    :param hub: The redistributed pop central hub
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    datas = []
    imps = []
    kwargs = {
        "s_path": opts.s_path,
        "cwd": os.getcwd(),
        "name": opts.name,
    }
    for imp in opts.imports:
        imp = imp.replace("\\", "\\\\")
        imps.append(imp)
    for data in opts.datas:
        src, dst = data.split(os.pathsep)
        src = src.replace("\\", "\\\\")
        dst = dst.replace("\\", "\\\\")
        datas.append((src, dst))

    # Freeze the packages that will be packaged into the binary and include the list
    # in a predictable location.
    # To use this file, your bundled app needs to read:
    #   `os.path.join(sys._MEIPASS, "app_freeze.txt")`
    freeze_file = os.path.join(opts.venv_dir, "app_freeze.txt")
    freeze_data = hub.tiamat.virtualenv.init.freeze(bname)
    with open(freeze_file, "w+") as fh_:
        fh_.write("\n".join(sorted(freeze_data)))
    datas.append((freeze_file, "."))

    kwargs["datas"] = datas.__repr__()
    kwargs["imports"] = imps.__repr__()
    kwargs["binaries"] = opts.get("binaries", []).__repr__()
    kwargs["runtime_tmpdir"] = opts.get("pyinstaller_runtime_tmpdir", None)
    if isinstance(kwargs["runtime_tmpdir"], str):
        kwargs["runtime_tmpdir"] = kwargs["runtime_tmpdir"].__repr__()
    if "--onedir" in hub.tiamat.BUILDS[bname].pypi_args:
        kwargs["onedir"] = True
        kwargs["name"] = "run"
        spec = SPEC.format(**kwargs)
        spec = spec + SPEC_COLL.format(**kwargs)
    else:
        kwargs["onedir"] = False
        spec = SPEC.format(**kwargs)
        spec = spec + SPEC_EXE.format(**kwargs)
    with open(opts.spec, "w+") as wfh:
        wfh.write(spec)
    opts.cmd.append(opts.spec)


def call(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    dname = os.path.dirname(opts.s_path)
    if not os.path.isdir(dname):
        os.makedirs(os.path.dirname(opts.s_path))
    shutil.copy(opts.run, opts.s_path)
    hub.tiamat.cmd.run(opts.cmd, timeout=opts.timeout, fail_on_error=True)
