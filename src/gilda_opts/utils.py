"""Utility functions and elements."""

import sys
from numbers import Number


if sys.version_info.minor >= 11:
    from typing import List, Dict, Any

    NumberSched = float | List[float] | Dict[str, float]
    IntSched = int | List[int] | Dict[str, int]
else:
    from typing import Any

    NumberSched = Any
    IntSched = Any


def get_number_at(var, index, def_value=None):
    """Return the number value from the scalar or list.

    :param var: scalar or list
    :param index: list index
    :param def_value: default value
    :returns: the scalar value or the indexed list number

    """
    if var is None:
        return def_value

    if isinstance(var, list):
        try:
            return var[index]
        except IndexError:
            return def_value

    if isinstance(var, dict):
        try:
            return var[str(index)]
        except KeyError:
            return def_value

    return var if isinstance(var, Number) else def_value
