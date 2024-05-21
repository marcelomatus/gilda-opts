from gilda_opts.demand import Demand


def test_demand_1():
    o1 = Demand(name='base', uid=1)

    assert o1.name == 'base'
    assert o1.uid == 1
    assert o1.load == 0

    o2 = Demand(uid=2, name='d2', load=1.0)

    assert o2.name == 'd2'
    assert o2.uid == 2
    assert o2.load == 1

