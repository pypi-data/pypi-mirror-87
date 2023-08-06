# noqa: D205,D208,D400
"""
    formelsammlung.envvar
    ~~~~~~~~~~~~~~~~~~~~~

    Get environment variables and transform their type.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
import os
import re

from typing import Any, Iterable, Optional


TRUE_BOOL_VALUES = ("1", "y", "yes", "t", "True")
FALSE_BOOL_VALUES = ("0", "n", "no", "f", "False")


def getenv_typed(
    var_name: str,
    default: Any = None,
    rv_type: Optional[type] = None,
    *,
    raise_error_if_no_value: bool = False,
    true_bool_values: Optional[Iterable] = None,
    false_bool_values: Optional[Iterable] = None,
) -> Any:
    """Wrap :func:`os.getenv` to adjust the type of the values.

    Instead of returning the environments variable's value as :class:`str` like
    :func:`os.getenv` you can set ``rv_type`` to a type to convert the value to. If
    ``rv_type`` is not set the type gets guessed and used for conversion.

    Guessable types are:

        - :class:`bool`
        - :class:`int`
        - :class:`float`
        - :class:`str` (fallback)

    How to use:

    .. testsetup::

        import os
        from formelsammlung.envvar import getenv_typed

    .. doctest::

        >>> os.environ["TEST_ENV_VAR"] = "2"
        >>> getenv_typed("TEST_ENV_VAR", 1, int)
        2

    .. testcleanup::

        os.environ["TEST_ENV_VAR"] = ""

    :param var_name: Name of the environment variable.
    :param default: Default value if no value is found for ``var_name``.
        Default: ``None``.
    :param rv_type: Type the value of the environment variable should be changed into.
        If not set or set to ``None`` the type gets guessed.
        Default: ``None``.
    :param raise_error_if_no_value: If ``True`` raises an :class:`KeyError` when no
        value is found for ``var_name`` and ``default`` is ``None``.
        Parameter is keyword only.
        Default: ``False``
    :param true_bool_values: Set of objects whose string representations are
        matched case-insensitive against the environment variable's value if the
        ``rv_type`` is :class:`bool` or the type gets guessed. If a match is found
        ``True`` is returned.
        Parameter is keyword only.
        Default: ``(1, "y", "yes", "t", True)``
    :param false_bool_values: Set of objects whose string representations are
        matched case-insensitive against the environment variable's value if the
        ``rv_type`` is :class:`bool` or the type gets guessed. If a match is found
        ``False`` is returned.
        Parameter is keyword only.
        Default: ``(0, "n", "no", "f", False)``
    :raises KeyError: If ``raise_error_if_no_value`` is ``True`` and no value is found
        for ``var_name`` and ``default`` is ``None``.
    :raises KeyError: If ``rv_type`` is set to :class:`bool` and value from
        ``var_name`` or ``default`` is not found in ``true_bool_values`` or
        ``false_bool_values``.
    :return: Value for ``var_name`` or ``default`` converted to ``rv_type``
        or guessed type.
    """
    env_var = os.getenv(var_name, default)

    if not env_var and default is None:
        if raise_error_if_no_value:
            raise KeyError(
                f"Environment variable '{var_name}' not set or empty and no default."
            ) from None
        return None

    #: Convert to given `rv_type` if set.
    if rv_type and rv_type is not bool:
        return rv_type(env_var)

    env_var = str(env_var)

    #: Guess bool value
    true_bool_values = set(true_bool_values or TRUE_BOOL_VALUES)
    false_bool_values = set(false_bool_values or FALSE_BOOL_VALUES)

    if env_var.casefold() in (str(b).casefold() for b in true_bool_values):
        return True
    if env_var.casefold() in (str(b).casefold() for b in false_bool_values):
        return False
    if rv_type:
        raise KeyError(
            f"Environment variable '{var_name}' has an invalid Boolean value.\n"
            f"For true use any of: {true_bool_values}\n"
            f"For false use any of: {false_bool_values}"
        ) from None

    #: Guess if `int`
    if re.fullmatch(r"^\d+$", env_var):
        env_var = int(env_var)

    #: Guess if `float`
    elif re.fullmatch(r"^\d+\.\d+$", env_var):
        env_var = float(env_var)

    return env_var
