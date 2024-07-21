"""Test demand module."""

from gilda_opts.demand import Demand


def test_demand_1():
    """Test demand 1."""
    o1 = Demand(name="base", uid=1, load_sched=[1, 2, 3])

    assert o1.name == "base"
    assert o1.uid == 1
    assert o1.load_sched == [1, 2, 3]

    o2 = Demand(uid=2, name="d2", load_sched=[1, 2, 3])

    assert o2.name == "d2"
    assert o2.uid == 2
    assert o2.load_sched == [1, 2, 3]

    o3 = Demand.from_json(o1.to_json())

    assert o1 == o3

    o1 = o3
    assert o1.name == "base"
    assert o1.uid == 1
    assert o1.load_sched == [1, 2, 3]
