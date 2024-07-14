"""Test tssa module."""

from gilda_opts.tssa import TSSA


def test_tssa_1():
    """test tssa 1."""
    o1 = TSSA(name="base", uid=1, on_period=2, load=3)

    assert o1.name == "base"
    assert o1.uid == 1
    assert o1.on_period == 2
    assert o1.load == 3

    o2 = TSSA(uid=2, name="d2", on_period=3, load=3)

    assert o2.name == "d2"
    assert o2.uid == 2
    assert o2.on_period == 3
    assert o2.load == 3

    o3 = TSSA.from_json(o1.to_json())

    assert o1 == o3

    o1 = o3
    assert o1.name == "base"
    assert o1.uid == 1
    assert o1.on_period == 2
    assert o1.load == 3
