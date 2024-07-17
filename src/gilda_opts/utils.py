"""Utility functions and elements."""

from numbers import Number
from typing import List, Dict, Any

NumberSched = float | List[float] | Dict[str | int, float]
IntSched = int | List[int] | Dict[str | int, int]


def get_value_at(var: NumberSched | IntSched, index: int, def_value: Any | None = None):
    """Return the number value from the scalar or list.

    :param var: scalar or list
    :param index: list index
    :param def_value: default value
    :returns: the scalar value or the indexed list number

    """
    if var is None:
        return def_value

    if isinstance(var, list):
        value = def_value
        try:
            value = var[index]
        except IndexError:
            pass
        return value

    if isinstance(var, dict):
        value = def_value
        try:
            value = var[str(index)]
        except KeyError:
            try:
                value = var[index]
            except KeyError:
                pass
        return value

    return var if isinstance(var, Number) else def_value
