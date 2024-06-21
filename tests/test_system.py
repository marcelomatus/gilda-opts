"""Test system module."""
from gilda_opts.system import System


def test_system_1():
    """Test system 1."""
    ds = '''{
      "name": "s1",
      "uid": 1,
      "buses": [{"uid": 1,
                 "name": "home"},
                {"uid": 2,
                 "name": "casa"}],
     "demands": [{"name": "d1",
                   "loads": [1, 2, 3, 4]}]
    }'''

    s1 = System.from_json(ds)

    assert s1.name == 's1'
    assert s1.uid == 1
    assert s1.buses[0].name == 'home'
    assert s1.buses[0].uid == 1
    assert s1.buses[1].name == 'casa'
    assert s1.buses[1].uid == 2

    assert s1.demands[0].name == 'd1'
    assert s1.demands[0].loads == [1, 2, 3, 4]
