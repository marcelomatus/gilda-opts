"""Test demand_grid_tssa_bess."""

from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP


def test_demanad_grid_tssas_bess():
    """Test system lp 5."""

    ds = """{
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
                  "load_sched": [1, 2, 3, 4]}],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 30,
                "energy_buy_price_sched": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factor_sched": [0,1,1,0]}],
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
            "max_flow_in": 3,
            "max_flow_out": 3,
            "efficiency_in": 0.5,
            "efficiency_out": 0.5
        }]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s2"
    assert s1.uid == 1
    assert s1.buses[0].name == "home"
    assert s1.buses[0].uid == 1

    assert s1.demands[0].name == "d1"
    assert s1.demands[0].load_sched == [1, 2, 3, 4]

    assert s1.grids[0].name == "g1"
    assert s1.grids[0].capacity == 30

    s1_lp = SystemLP(s1)

    status = s1_lp.solve(keepfiles=False)

    assert status == "ok"

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.demands_lp[1].load_cols[0]) == 1
    assert lp.get_col_at(s1_lp.demands_lp[1].load_cols[1]) == 2
    assert lp.get_col_at(s1_lp.demands_lp[1].load_cols[2]) == 3
    assert lp.get_col_at(s1_lp.demands_lp[1].load_cols[3]) == 4

    assert lp.get_col_at(s1_lp.tssas_lp[1].onoff_cols[0]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].onoff_cols[1]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].onoff_cols[2]) == 1
    assert lp.get_col_at(s1_lp.tssas_lp[1].onoff_cols[3]) == 1

    assert lp.get_col_at(s1_lp.besss_lp[1].flow_in_cols[0]) == 3
    assert lp.get_col_at(s1_lp.besss_lp[1].flow_in_cols[1]) == 0.2
    assert lp.get_col_at(s1_lp.besss_lp[1].flow_in_cols[2]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].flow_in_cols[3]) == 0

    assert lp.get_col_at(s1_lp.besss_lp[1].flow_out_cols[0]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].flow_out_cols[1]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].flow_out_cols[2]) == 0.8
    assert lp.get_col_at(s1_lp.besss_lp[1].flow_out_cols[3]) == 0.0

    assert lp.get_col_at(s1_lp.besss_lp[1].efin_cols[0]) == 1.5
    assert lp.get_col_at(s1_lp.besss_lp[1].efin_cols[1]) == 1.6
    assert lp.get_col_at(s1_lp.besss_lp[1].efin_cols[2]) == 0
    assert lp.get_col_at(s1_lp.besss_lp[1].efin_cols[3]) == 0

    withdrawn_values = lp.get_col_sol(s1_lp.grids_lp[1].withdrawn_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].load_cols)

    assert (withdrawn_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 5.2

    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[0]) == 7
    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[1]) == 5.2
    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[2]) == 5.2
    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[3]) == 7

    assert lp.get_obj() == 5000 * 5.2 + 11 * 7 + 12 * 5.2 + 13 * 5.2 + 14 * 7

    s1_sched = s1_lp.get_sched()
    assert s1_sched.name == s1.name
