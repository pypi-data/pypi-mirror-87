"""
    formelsammlung.venv_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Utility function for working with virtual environments.

    :copyright: 2020 (c) Christian Riedel
    :license: GPLv3, see LICENSE file for more details
"""  # noqa: D205, D208, D400
import os
import shutil
import sys

from pathlib import Path
from typing import Optional, Tuple, Union


OS_BIN = "Scripts" if sys.platform == "win32" else "bin"


def get_venv_path() -> Path:
    """Get path to the venv from where the python executable runs.

    :raises FileNotFoundError: when no calling venv can be detected.
    :return: Return venv path
    """
    if hasattr(sys, "real_prefix"):
        return Path(sys.real_prefix)  # type: ignore[no-any-return,attr-defined] # pylint: disable=E1101
    if sys.base_prefix != sys.prefix:
        return Path(sys.prefix)
    raise FileNotFoundError("No calling venv could be detected.")


def get_venv_bin_dir(venv_path: Union[str, Path]) -> Path:
    """Return path to bin/Scripts dir of given venv.

    :param venv_path: Path to venv
    :raises FileNotFoundError: when no bin/Scripts dir can be found for given venv.
    :return: Path to bin/Scripts dir
    """
    bin_dir = Path(venv_path) / OS_BIN
    if bin_dir.is_dir():
        return bin_dir

    raise FileNotFoundError(f"Given venv has no '{OS_BIN}' directory.")


def get_venv_tmp_dir(venv_path: Union[str, Path]) -> Path:
    """Return path to tmp/temp dir of given venv.

    :param venv_path: Path to venv
    :raises FileNotFoundError: when no tmp/temp dir can be found for given venv.
    :return: Path to tmp/temp dir
    """
    tmp_dir = Path(venv_path) / "tmp"
    if tmp_dir.is_dir():
        return tmp_dir

    tmp_dir = Path(venv_path) / "temp"
    if tmp_dir.is_dir():
        return tmp_dir

    raise FileNotFoundError("Given venv has no 'tmp' or 'temp' directory.")


def get_venv_site_packages_dir(venv_path: Union[str, Path]) -> Path:
    """Return path to site-packages dir of given venv.

    :param venv_path: Path to venv
    :raises FileNotFoundError: when no site-packages dir can be found for given venv.
    :return: Path to site-packages dir
    """
    paths = list(Path(venv_path).glob("**/site-packages"))
    if paths:
        return paths[0]

    raise FileNotFoundError("Given venv has no 'site-packages' directory.")


def where_installed(program: str) -> Tuple[int, Optional[str], Optional[str]]:
    """Find installation locations for given program.

    Return exit code and locations based on found installation places.
    Search in current venv and globally.

    Exit codes:

    - 0 = nowhere
    - 1 = venv
    - 2 = global
    - 3 = both

    :param program: Program to search
    :return: Exit code, venv executable path, glob executable path
    """
    exit_code = 0

    exe = shutil.which(program)
    if not exe:
        return exit_code, None, None

    venv_path = get_venv_path()
    bin_dir = "\\Scripts" if sys.platform == "win32" else "/bin"
    path_wo_venv = os.environ["PATH"].replace(f"{venv_path}{bin_dir}", "")
    glob_exe = shutil.which(program, path=path_wo_venv)

    if glob_exe is None:
        exit_code += 1
    elif exe == glob_exe:
        exit_code += 2
        exe = None
    else:
        exit_code += 3
    return exit_code, exe, glob_exe
