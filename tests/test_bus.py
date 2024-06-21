"""Test bus module."""

from gilda_opts.bus import Bus
from gilda_opts.bus_lp import BusLP


def test_bus_1():
    """Test bus 1."""

    b1 = Bus(name='home', uid=1)

    assert b1.name == 'home'
    assert b1.uid == 1

    b2 = Bus(uid=2, name='home2')

    assert b2.name == 'home2'
    assert b2.uid == 2


def test_bus_2():
    """Test bus 2."""

    data = '{"name": "home", "uid": 1}'

    b1 = Bus.from_json(data)

    assert b1.name == 'home'
    assert b1.uid == 1

    d1 = b1.to_json()

    b2 = Bus.from_json(d1)

    assert b2 == b1


def test_bus_3():
    """Test bus 3."""

    data = '{"name": "home", "uid": 1}'

    b1 = Bus.from_json(data)

    b1_lp = BusLP(bus=b1)

    assert b1 == b1_lp.bus
