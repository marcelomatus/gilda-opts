"""Test demand_grid."""
from pytest import approx

from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP


def test_demand_grid__line_1():
    """Test system_lp 1."""
    ds = """{
      "name": "s1",
      "uid": 1,
      "blocks": [{"duration": 1},
                 {"duration": 1},
                 {"duration": 1},
                 {"duration": 1}],
      "buses": [{"uid": 1,
                 "name": "b1"},
                {"uid": 2,
                 "name": "b2"}],
      "demands": [{"name": "d1",
                  "uid": 1,
                  "bus_uid": 1,
                  "load_sched": [1, 2, 3, 4]}],
      "lines": [{"name": "l1",
                 "uid": 1,
                 "capacity": 100,
                 "bus_a_uid": 2,
                 "bus_b_uid": 1
                }],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 2,
                "capacity": 30,
                "energy_buy_price_sched": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factor_sched": [0,1,1,0]}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
    assert s1.uid == 1
    assert s1.buses[0].name == "b1"
    assert s1.buses[0].uid == 1

    assert s1.buses[1].name == "b2"
    assert s1.buses[1].uid == 2

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

    withdrawn_values = lp.get_col_sol(s1_lp.grids_lp[1].withdrawn_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].load_cols)

    assert (withdrawn_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == 3
    assert lp.get_obj() == 5000 * 3 + 11 * 1 + 12 * 2 + 13 * 3 + 14 * 4

    s1_sched = s1_lp.get_sched()

    assert s1_sched.name == s1.name

    assert s1_sched.lines[0].flow_values[0] == 1
    assert s1_sched.lines[0].flow_values[1] == 2
    assert s1_sched.lines[0].flow_values[2] == 3
    assert s1_sched.lines[0].flow_values[3] == 4


def test_demand_grid_line_2():
    """Test system_lp 1."""
    ds = """{
      "name": "s1",
      "uid": 1,
      "blocks": [{"duration": 1},
                 {"duration": 1},
                 {"duration": 1},
                 {"duration": 1}],
      "buses": [{"uid": 1,
                 "name": "b1"},
                {"uid": 2,
                 "name": "b2"}],
      "demands": [{"name": "d1",
                  "uid": 1,
                  "bus_uid": 1,
                  "load_sched": [1, 2, 3, 4]}],
      "lines": [{"name": "l1",
                 "uid": 1,
                 "capacity": 100,
                 "losses": 0.1,
                 "bus_a_uid": 1,
                 "bus_b_uid": 2
                }],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 2,
                "capacity": 30,
                "energy_buy_price_sched": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factor_sched": [0,1,1,0]}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
    assert s1.uid == 1
    assert s1.buses[0].name == "b1"
    assert s1.buses[0].uid == 1

    assert s1.buses[1].name == "b2"
    assert s1.buses[1].uid == 2

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

    withdrawn_values = lp.get_col_sol(s1_lp.grids_lp[1].withdrawn_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].load_cols)

    assert (withdrawn_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == approx(3.33333333)

    s1_sched = s1_lp.get_sched()

    assert s1_sched.name == s1.name

    assert s1_sched.lines[0].flow_values[0] == approx(-1.1111111111)
    assert s1_sched.lines[0].flow_values[1] == approx(-2.2222222222)
    assert s1_sched.lines[0].flow_values[2] == approx(-3.3333333333)
    assert s1_sched.lines[0].flow_values[3] == approx(-4.4444444444)


def test_demand_grid_line_3():
    """Test system_lp 1."""
    ds = """{
      "name": "s1",
      "uid": 1,
      "blocks": [{"duration": 1},
                 {"duration": 1},
                 {"duration": 1},
                 {"duration": 1}],
      "buses": [{"uid": 1,
                 "name": "b1"},
                {"uid": 2,
                 "name": "b2"}],
      "demands": [{"name": "d1",
                  "uid": 1,
                  "bus_uid": 1,
                  "load_sched": [1, 2, 3, 4]}],
      "lines": [{"name": "l1",
                 "uid": 1,
                 "capacity": 100,
                 "losses": 0.1,
                 "bus_a_uid": 2,
                 "bus_b_uid": 1
                }],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 2,
                "capacity": 30,
                "energy_buy_price_sched": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factor_sched": [0,1,1,0]}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
    assert s1.uid == 1
    assert s1.buses[0].name == "b1"
    assert s1.buses[0].uid == 1

    assert s1.buses[1].name == "b2"
    assert s1.buses[1].uid == 2

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

    withdrawn_values = lp.get_col_sol(s1_lp.grids_lp[1].withdrawn_cols)
    load_values = lp.get_col_sol(s1_lp.demands_lp[1].load_cols)

    assert (withdrawn_values == load_values).all()

    assert lp.get_col_at(s1_lp.grids_lp[1].pmax_col) == approx(3.33333333)

    s1_sched = s1_lp.get_sched()

    assert s1_sched.name == s1.name

    assert s1_sched.lines[0].flow_values[0] == approx(1.1111111111)
    assert s1_sched.lines[0].flow_values[1] == approx(2.2222222222)
    assert s1_sched.lines[0].flow_values[2] == approx(3.3333333333)
    assert s1_sched.lines[0].flow_values[3] == approx(4.4444444444)
