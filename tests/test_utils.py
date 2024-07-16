"""Test utilities module."""

from gilda_opts.utils import get_number_at


def test_utils_1():
    """Test get_number_at."""
    assert get_number_at(3, 0) == 3
    assert get_number_at([3], 0) == 3
    assert get_number_at([3], 1, 0) == 0
