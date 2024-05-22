from gilda_opts.system import System, SystemOptions


def test_system_1():
    opts = SystemOptions()
    assert opts.cfail == 1000
    assert opts.integer_mode == 0


def test_system_2():

    ds = '''{
      "name": "s1",
      "uid": 1,
      "options": {"cfail": 500,
                  "integer_mode": 1},
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
    assert s1.options.cfail == 500
    assert s1.options.integer_mode == 1
    assert s1.buses[0].name == 'home'
    assert s1.buses[0].uid == 1
    assert s1.buses[1].name == 'casa'
    assert s1.buses[1].uid == 2

    assert s1.demands[0].name == 'd1'
    assert s1.demands[0].loads == [1, 2, 3, 4]
