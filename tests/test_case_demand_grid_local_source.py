"""Test demand_grid_tssa."""

from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP


def test_demand_grid_local_source():
    """Test system_lp 1."""
    ds = """{
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
                  "load_sched": [1, 2, 3, 4]}],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 30,
                "energy_buy_price_sched": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factor_sched": [0,1,1,0],
                "energy_sell_price_sched": [5, 6, 7, 8]}],
      "local_sources": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 20,
                "generation_profile_sched": [0, 1, 0, 0.5]}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
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

    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[0]) == 1
    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[1]) == 0
    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[2]) == 3
    assert lp.get_col_at(s1_lp.grids_lp[1].withdrawn_cols[3]) == 0

    assert lp.get_col_at(s1_lp.local_sources_lp[1].generation_cols[0]) == 0
    assert lp.get_col_at(s1_lp.local_sources_lp[1].generation_cols[1]) == 20
    assert lp.get_col_at(s1_lp.local_sources_lp[1].generation_cols[2]) == 0
    assert lp.get_col_at(s1_lp.local_sources_lp[1].generation_cols[3]) == 10

    withdrawn_values = lp.get_col_sol(s1_lp.grids_lp[1].withdrawn_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].load_cols)

    assert (withdrawn_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 3
    assert lp.get_obj() == 5000 * 3 + 11 * 1 + 12 * 0 + 13 * 3 + 14 * 0 - 6 * 18 - 8 * 6
