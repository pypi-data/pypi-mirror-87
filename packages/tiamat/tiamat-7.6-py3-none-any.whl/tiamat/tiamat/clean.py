import logging
import os
import shutil
from typing import Callable
from typing import Tuple

log = logging.getLogger(__name__)
__func_alias__ = {"all_": "all"}


def _report_error(_, path: str, error: Tuple[Callable, Exception]):
    if error[0] is FileNotFoundError:
        log.debug(f"File {path} is already deleted")
    else:
        log.error(error[1])


def remove_dist(hub, directory: str):
    """
    Clean the resulting dist dir

    This is in it's own function in case one day someone adds the --distpath option to
    the pyinstaller call
    """
    dist_dir = os.path.join(directory, "dist")
    hub.log.info(f"Removing {dist_dir}")
    shutil.rmtree(dist_dir, onerror=_report_error)


def remove_build(hub, directory: str):
    """
    Clean the build dir
    This is in it's own function in case one day someone adds the --workpath option to
    the pyinstaller call
    """
    build_dir = os.path.join(directory, "build")
    hub.log.info(f"Removing {build_dir}")
    shutil.rmtree(os.path.join(directory, "build"), onerror=_report_error)


def remove_pytest_cache(hub, directory: str):
    """
    Remove the pytest cache
    """
    pycache_dir = os.path.join(directory, ".pytest_cache")
    hub.log.info(f"Removing {pycache_dir}")
    shutil.rmtree(pycache_dir, onerror=_report_error)


def remove_logs(hub, directory: str):
    """
    Recursively remove all files ending in .log from the build directory
    """
    for parent, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".log"):
                log_file = os.path.join(parent, f)
                hub.log.info(f"Removing {log_file}")
                try:
                    os.remove(log_file)
                except Exception as e:
                    _report_error(_, log_file, (type(e), e))


def all_(hub, directory: str):
    """
    Run all the functions in this plugin
    """
    for func in hub.tiamat.clean:
        if func.__name__ == "all":
            # Skip this function or we would have an infinite loop
            continue

        func(directory)
