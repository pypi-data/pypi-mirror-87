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


def get_venv_path(raise_error: bool = False) -> Optional[Path]:
    """Get path to the venv from where the python executable runs.

    :param raise_error: raise FileNotFoundError if no venv is detected.
        Default: ``False``
    :raises FileNotFoundError: when no calling venv can be detected.
    :return: Return venv path or None if python is not called from a venv.
    """
    if hasattr(sys, "real_prefix"):
        return Path(sys.real_prefix)  # type: ignore[no-any-return,attr-defined] # pylint: disable=E1101
    if sys.base_prefix != sys.prefix:
        return Path(sys.prefix)
    if raise_error:
        raise FileNotFoundError("No calling venv could be detected.")
    return None


def get_venv_bin_dir(
    venv_path: Union[str, Path], raise_error: bool = False
) -> Optional[Path]:
    """Return path to bin/Scripts dir of given venv.

    :param venv_path: Path to venv
    :param raise_error: raise FileNotFoundError if no bin/Scripts dir is found.
        Default: ``False``
    :raises FileNotFoundError: when no bin/Scripts dir can be found for given venv.
    :return: Path to bin/Scripts dir or None
    """
    bin_dir = Path(venv_path) / OS_BIN

    if not bin_dir.is_dir():
        if raise_error:
            raise FileNotFoundError(f"Given venv has no '{OS_BIN}' directory.")
        return None
    return bin_dir


def get_venv_tmp_dir(
    venv_path: Union[str, Path], raise_error: bool = False
) -> Optional[Path]:
    """Return path to tmp/temp dir of given venv.

    :param venv_path: Path to venv
    :param raise_error: raise FileNotFoundError if no tmp/temp dir is found.
        Default: ``False``
    :raises FileNotFoundError: when no tmp/temp dir can be found for given venv.
    :return: Path to tmp/temp dir or None
    """
    tmp_dir = Path(venv_path) / "tmp"
    if not tmp_dir.is_dir():
        tmp_dir = Path(venv_path) / "temp"
        if not tmp_dir.is_dir():
            if raise_error:
                raise FileNotFoundError("Given venv has no 'tmp' or 'temp' directory.")
            return None
    return tmp_dir


def get_venv_site_packages_dir(
    venv_path: Union[str, Path], raise_error: bool = False
) -> Optional[Path]:
    """Return path to site-packages dir of given venv.

    :param venv_path: Path to venv
    :param raise_error: raise FileNotFoundError if no site-packages dir is found.
        Default: ``False``
    :raises FileNotFoundError: when no site-packages dir can be found for given venv.
    :return: Path to site-packages dir or None
    """
    paths = list(Path(venv_path).glob("**/site-packages"))

    if not paths:
        if raise_error:
            raise FileNotFoundError("Given venv has no 'site-packages' directory.")
        return None
    return paths[0]


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
