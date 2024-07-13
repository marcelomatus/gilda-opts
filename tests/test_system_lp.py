"""Test system_lp."""
from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP


def test_system_lp_1():
    """Test system_lp 1."""
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

    status = s1_lp.solve(keepfiles=False)

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
    """Test system lp 2."""
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

    status = s1_lp.solve(keepfiles=False)

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
    """Test system lp 3."""

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

    status = s1_lp.solve(keepfiles=False)

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


def test_system_lp_4():
    """Test system lp 4."""

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
            "on_period": 4
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

    status = s1_lp.solve(keepfiles=False)

    assert status == 'ok'

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[3]) == 4

    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[0]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[1]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[2]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[3]) == 1

    injection_values = lp.get_col_sol(s1_lp.grids_lp[1].block_injection_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].block_load_cols)

    assert (injection_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 6
    assert lp.get_obj() == 5000*6 + 11*4 + 12*5 + 13*6 + 14*7


def test_system_lp_5():
    """Test system lp 5."""

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
            "on_period": 4
        }],
      "besss": [{
            "uid": 1,
            "name": "b1",
            "bus_uid": 1,
            "capacity": 20,
            "max_flow": 3,
            "efficiency": 0.5
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

    status = s1_lp.solve(keepfiles=True)

    assert status == 'ok'

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[3]) == 4

    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[0]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[1]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[2]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].block_onoff_cols[3]) == 1

    assert lp.get_col_at(s1_lp.besss_lp[1].block_inflow_cols[0]) == 3
    assert lp.get_col_at(s1_lp.besss_lp[1].block_inflow_cols[1]) == 0.2
    assert lp.get_col_at(s1_lp.besss_lp[1].block_inflow_cols[2]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].block_inflow_cols[3]) == 0

    assert lp.get_col_at(s1_lp.besss_lp[1].block_outflow_cols[0]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].block_outflow_cols[1]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].block_outflow_cols[2]) == 0.8
    assert lp.get_col_at(s1_lp.besss_lp[1].block_outflow_cols[3]) == 0.0

    assert lp.get_col_at(s1_lp.besss_lp[1].block_efin_cols[0]) == 1.5
    assert lp.get_col_at(s1_lp.besss_lp[1].block_efin_cols[1]) == 1.6
    assert lp.get_col_at(s1_lp.besss_lp[1].block_efin_cols[2]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].block_efin_cols[3]) == 0

    injection_values = lp.get_col_sol(s1_lp.grids_lp[1].block_injection_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].block_load_cols)

    assert (injection_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 5.2

    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[0]) == 7
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[1]) == 5.2
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[2]) == 5.2
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[3]) == 7

    assert lp.get_obj() == 5000*5.2 + 11*7 + 12*5.2 + 13*5.2 + 14*7


def test_system_lp_6():
    """Test system_lp 1."""
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
                "power_factors": [0,1,1,0],
                "energy_sell_prices": [5, 6, 7, 8]}],
      "local_sources": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 20,
                "generation_profile": [0, 1, 0, 0.5]}]
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

    status = s1_lp.solve(keepfiles=False)

    assert status == 'ok'

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].block_load_cols[3]) == 4

    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[0]) == 1
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[1]) == 0
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[2]) == 3
    assert lp.get_col_at(s1_lp.grids_lp[1].block_injection_cols[3]) == 0

    assert lp.get_col_at(s1_lp.local_sources_lp[1].block_injection_cols[0]) == 0
    assert lp.get_col_at(s1_lp.local_sources_lp[1].block_injection_cols[1]) == 20
    assert lp.get_col_at(s1_lp.local_sources_lp[1].block_injection_cols[2]) == 0
    assert lp.get_col_at(s1_lp.local_sources_lp[1].block_injection_cols[3]) == 10

    injection_values = lp.get_col_sol(s1_lp.grids_lp[1].block_injection_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].block_load_cols)

    assert (injection_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 3
    assert lp.get_obj() == 5000*3 + 11*1 + 12*0 + 13*3 + 14*0 - 6*18 -8*6
