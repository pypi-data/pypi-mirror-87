import os
import shutil
import sys


def report(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    art = os.path.abspath(os.path.join("dist", opts.name))

    # This is the only print statement from the program, everything else gets logged
    # through stderr
    print(art, file=sys.stdout, flush=True)

    # Save the location of the result to an environment variable for CICD or
    # wrapper scripts
    os.environ["TIAMAT_BUILD_PACKAGE"] = art


def clean(hub, bname: str):
    """
    :param hub: The redistributed pop central hub.
    :param bname: The name of the build configuration to use from the build.conf file.
    """
    opts = hub.tiamat.BUILDS[bname]
    shutil.rmtree(opts.venv_dir)
    os.remove(opts.spec)
    os.remove(opts.req)
    try:
        # try to remove pyinstaller warn-*** file
        os.remove(os.path.join(opts.dir, "build", opts.name, f"warn-{opts.name}.txt"))
    except FileNotFoundError:
        pass
