"""Utility functions and elements."""

from numbers import Number


def get_number_at(var, index, def_value=None):
    """Return the number value from the scalar or list.

    :param var: scalar or list
    :param index: list index
    :param def_value: default value
    :returns: the scalar value or the indexed list number

    """
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
