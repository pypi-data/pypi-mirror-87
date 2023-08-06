# noqa: D205,D208,D400
"""
    formelsammlung
    ~~~~~~~~~~~~~~

    Collection of different multipurpose functions.

    :copyright: (c) Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version  # type: ignore[import,no-redef]

__version__ = version(__name__)
