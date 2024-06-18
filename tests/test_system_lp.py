
from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP


def test_system_lp_1():

    ds = '''{
      "name": "s1",
      "uid": 1,
      "blocks": [{"duration": 1},
                 {"duration": 1},
                 {"duration": 1},
                 {"duration": 1}],
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

    s1_lp = SystemLP(s1)
    assert s1_lp == s1_lp

    status = s1_lp.solve(keepfiles=True)

    assert status == 'ok'

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[3]) == 4

    injection_values = lp.get_col_sol(s1_lp.grids_lp[1].block_injection_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].block_load_cols)

    assert (injection_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 3
    assert lp.get_obj() == 5000*3 + 11*1 + 12*2 + 13*3 + 14*4


def test_system_lp_2():

    ds = '''{
      "name": "s2",
      "uid": 1,
      "blocks": [{"duration": 1},
                 {"duration": 1},
                 {"duration": 1},
                 {"duration": 1}],
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
                "power_factors": [0,1,1,0]}],
      "tssas": [{
            "uid": 1,
            "name": "lavado",
            "bus_uid": 1,
            "load": 3,
            "on_period": 1
        }]
    }'''

    s1 : System = System.from_json(ds)

    assert s1.name == 's2'
    assert s1.uid == 1
    assert s1.buses[0].name == 'home'
    assert s1.buses[0].uid == 1

    assert s1.demands[0].name == 'd1'
    assert s1.demands[0].loads == [1, 2, 3, 4]

    assert s1.grids[0].name == 'g1'
    assert s1.grids[0].capacity == 30

    s1_lp = SystemLP(s1)
    assert s1_lp == s1_lp

    status = s1_lp.solve(keepfiles=True)

    assert status == 'ok'

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[3]) == 4

    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[0]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[1]) == 0
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[2]) == 0
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[3]) == 0

    injection_values = lp.get_col_sol(s1_lp.grids_lp[1].block_injection_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].block_load_cols)

    assert (injection_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 3
    assert lp.get_obj() == 5000*3 + 11*(1+3) + 12*2 + 13*3 + 14*4


def test_system_lp_3():

    ds = '''{
      "name": "s2",
      "uid": 1,
      "blocks": [{"duration": 1},
                 {"duration": 1},
                 {"duration": 1},
                 {"duration": 1}],
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
                "power_factors": [0,1,1,0]}],
      "tssas": [{
            "uid": 1,
            "name": "lavado",
            "bus_uid": 1,
            "load": 3,
            "on_period": 2
        }]
    }'''

    s1 : System = System.from_json(ds)

    assert s1.name == 's2'
    assert s1.uid == 1
    assert s1.buses[0].name == 'home'
    assert s1.buses[0].uid == 1

    assert s1.demands[0].name == 'd1'
    assert s1.demands[0].loads == [1, 2, 3, 4]

    assert s1.grids[0].name == 'g1'
    assert s1.grids[0].capacity == 30

    s1_lp = SystemLP(s1)
    assert s1_lp == s1_lp

    status = s1_lp.solve(keepfiles=True)

    assert status == 'ok'

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[3]) == 4

    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[0]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[1]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[2]) == 0
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[3]) == 0

    injection_values = lp.get_col_sol(s1_lp.grids_lp[1].block_injection_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].block_load_cols)

    assert (injection_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 5

    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[0]) == 1 + 3
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[1]) == 2 + 3
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[2]) == 3
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[3]) == 4

    assert lp.get_obj() == 5000*5 + 11*(1+3) + 12*(2+3) + 13*3 + 14*4
