
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
                  "uid": 1,
                  "bus_uid": 1,
                  "loads": [1, 2, 3, 4]}],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 30,
                "energy_tariffs": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factors": [0,1,1,0]}]
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

    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[3]) == 4

    injection_values = lp.get_col_sol(s1_lp.grids_lp[1].block_injection_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].block_load_cols)

    assert (injection_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 3
    assert lp.get_obj() == 5000*3 + 11*1 + 12*2 + 13*3 + 14*4
