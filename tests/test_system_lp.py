
from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP


def test_system_lp_1():

    ds = '''{
      "name": "s1",
      "uid": 1,
      "buses": [{"uid": 1,
                 "name": "home"}],
      "demands": [{"name": "d1",
                  "bus_uid": 1,
                  "loads": [1, 2, 3, 4]}],
      "grids": [{"name": "g1",
                "bus_uid": 1,
                "capacity": 30,
                "energy_tariffs": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factors": [0,0,1,1]}]
    }'''

    s1 : System = System.from_json(ds)

    assert s1.name == 's1'
    assert s1.uid == 1
    assert s1.buses[0].name == 'home'
    assert s1.buses[0].uid == 1

    assert s1.demands[0].name == 'd1'
    assert s1.demands[0].loads == [1, 2, 3, 4]

    assert s1.grids[0].name == 'g1'
    assert s1.grids[0].capacity == 30

    lp = LinearProblem()
    s1_lp = SystemLP(s1, lp)
    assert s1_lp == s1_lp

    blocks = [Block(index=0, duration=1),
              Block(index=1, duration=1),
              Block(index=2, duration=1),
              Block(index=3, duration=1)]
    s1_lp.add_blocks(blocks)

    assert lp.numcols() == 9
    assert lp.numrows() == 6

    lp.solve(keepfiles=True)

    assert lp.get_status() == 'ok'
