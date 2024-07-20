"""Test utilities module."""

from gilda_opts.utils import get_value_at


def test_utils_1():
    """Test get_value_at."""
    assert get_value_at(3, 0) == 3
    assert get_value_at([3], 0) == 3
    assert get_value_at([3], 1, 0) == 0

    assert get_value_at({"3": 1.0}, 3) == 1.0
    assert get_value_at({"3": 1}, 2, 3) == 3

    assert get_value_at({3: 1}, 3) == 1
    assert get_value_at({3: 1}, 2, 3) == 3
