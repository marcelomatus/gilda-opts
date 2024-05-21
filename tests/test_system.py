
from gilda_opts.bus import Bus
from gilda_opts.system import System, SystemOptions


def test_system_1():
    opts = SystemOptions()
    assert opts.cfail == 1000
    assert opts.integer_mode == 0


def test_system_2():

    data = '[{"name": "home", "uid": 1}, {"name": "casa", "uid": 2}]'

    buses = Bus.schema().loads(data, many=True)

    s1 = System(name='s1', buses=buses)

    assert s1.name == 's1'

    data = s1.to_json()

    s2 = System.from_json(data)

    assert s1 == s2
