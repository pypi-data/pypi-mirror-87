"""
    formelsammlung.tox_env_exe_runner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Call tools from tox environments.

    :copyright: 2020 (c) Christian Riedel
    :license: GPLv3, see LICENSE file for more details
"""  # noqa: D205, D208, D400
import subprocess  # nosec
import sys

from pathlib import Path
from typing import List, Optional


def env_exe_runner(
    venv_runner: List[str],
    envs: List[str],
    tool: str,
    tool_args: Optional[List[str]] = None,
) -> int:
    """Call given ``tool`` from given `tox` or `nox` or `virtual` env considering OS.

    :param venv_runner: List containing: 'nox' and/or 'tox' and/or one or more
        'virtual environment's
    :param envs: List of environments to search the ``tool`` in when 'tox' or 'nox' is
        in venv_runner. If neither 'tox' nor 'nox' is in ``venv_runner`` you may pass
        an empty list.
    :param tool: Name of the executable to run.
    :param tool_args: Arguments to give to the ``tool``.
    :return: Exit code 127 if no executable is found or the exit code of the called cmd.
    """
    is_win = sys.platform == "win32"

    exe = Path(f"Scripts/{tool}.exe") if is_win else Path(f"bin/{tool}")
    cmd = None

    if not tool_args:
        tool_args = []

    for runner in venv_runner:
        if runner in ("tox", "nox"):
            for env in envs:
                path = Path(f".{runner}") / env / exe
                if path.is_file():
                    cmd = (str(path), *tool_args)
                    break
        else:
            path = Path(runner) / exe
            if path.is_file():
                cmd = (str(path), *tool_args)
        if cmd:
            break

    if cmd is None:
        print(f"No '{tool}' executable found. Search in:")
        for runner in venv_runner:
            if runner in ("tox", "nox"):
                print(f"- '{runner}' envs: {envs}")
            else:
                print(f"- virtual env: ['{runner}']")
        return 127

    return subprocess.call(cmd)  # nosec


def cli_caller() -> int:
    """Warp ``env_exe_runner`` to be callable by cli.

    Script to call executables in `tox`/`nox`/`virtual` envs considering OS.

    The script takes three mandatory arguments:

    1. A string with comma separated runner (`tox` and/or `nox`) and/or virtual envs.
    2. A string with comma separated `tox`/`nox` envs to check for the executable.
       The envs are checked in given order. If `tox`/`nox` are not part of the first arg
       you may pass a '-' as second arg.
    3. The executable to call like e.g. `pylint`.

    All other arguments after are passed to the tool on call.

    :return: Exit code from ``env_exe_runner``
    """
    return env_exe_runner(
        sys.argv[1].split(","), sys.argv[2].split(","), sys.argv[3], sys.argv[4:]
    )  # pragma: no cover


if __name__ == "__main__":
    sys.exit(cli_caller())
