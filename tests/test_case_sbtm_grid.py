"""Test demand_grid_tssa."""

from pytest import approx
from gilda_opts.system import System
from gilda_opts.system_lp import SystemLP


def test_sbtm_grid_1():
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
      "sbtms": [{"name": "home",
                  "uid": 1,
                  "bus_uid": 1,
                  "single_room": {
                      "total_floor_area": 70,
                      "height": 2.5,
                      "u_value": 2,
                      "air_renewal": 0.5,
                      "air_density": 1.225,
                      "air_specific_heat_capacity": 1.005,
                      "thermal_mass_parameter": 250.0,
                      "heating_power": 10,
                      "time_interval": 1800,
                      "initial_temperature": 20,
                      "external_temperatures": 20,
                      "thermal_drift_cost": 500}
                 }],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 30,
                "energy_tariffs": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factors": [0,1,1,0]}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
    assert s1.uid == 1
    assert s1.buses[0].name == "home"
    assert s1.buses[0].uid == 1

    assert s1.sbtms[0].name == "home"

    assert s1.grids[0].name == "g1"
    assert s1.grids[0].capacity == 30

    s1_lp = SystemLP(s1)

    status = s1_lp.solve(keepfiles=False)

    assert status == "ok"

    lp = s1_lp.lp

    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[0]) == 20
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[1]) == 20
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[2]) == 20
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[3]) == 20


def test_sbtm_grid_2():
    """Test system_lp 1."""
    ds = """{
      "name": "s1",
      "uid": 1,
      "blocks": [{"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5}],
      "buses": [{"uid": 1,
                 "name": "home"}],
      "sbtms": [{"name": "home",
                  "uid": 1,
                  "bus_uid": 1,
                  "single_room": {
                      "total_floor_area": 70,
                      "height": 2.5,
                      "u_value": 2,
                      "air_renewal": 0.5,
                      "air_density": 1.225,
                      "air_specific_heat_capacity": 1.005,
                      "thermal_mass_parameter": 250.0,
                      "heating_power": 10,
                      "time_interval": 1800,
                      "initial_temperature": 20,
                      "external_temperatures": 30,
                      "thermal_drift_cost": 500}
                 }],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 30,
                "energy_tariffs": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factors": [0,1,1,0]}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
    assert s1.uid == 1
    assert s1.buses[0].name == "home"
    assert s1.buses[0].uid == 1

    assert s1.sbtms[0].name == "home"

    assert s1.grids[0].name == "g1"
    assert s1.grids[0].capacity == 30

    s1_lp = SystemLP(s1)

    status = s1_lp.solve(keepfiles=False)

    assert status == "ok"

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[0]) == approx(20.490891)
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[1]) == approx(20.957685)


def test_sbtm_grid_3():
    """Test system_lp 1."""
    ds = """{
      "name": "s1",
      "uid": 1,
      "blocks": [{"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5}],
      "buses": [{"uid": 1,
                 "name": "home"}],
      "sbtms": [{"name": "home",
                  "uid": 1,
                  "bus_uid": 1,
                  "single_room": {
                      "total_floor_area": 70,
                      "height": 2.5,
                      "u_value": 2,
                      "air_renewal": 0.5,
                      "air_density": 1.225,
                      "air_specific_heat_capacity": 1.005,
                      "thermal_mass_parameter": 250.0,
                      "heating_power": 10,
                      "time_interval": 1800,
                      "initial_temperature": 20,
                      "external_temperatures": 10,
                      "thermal_drift_cost": 500}
                 }],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 30,
                "energy_tariffs": [11, 12, 13, 14],
                "power_tariff": 5000,
                "power_factors": [0,1,1,0]}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
    assert s1.uid == 1
    assert s1.buses[0].name == "home"
    assert s1.buses[0].uid == 1

    assert s1.sbtms[0].name == "home"

    assert s1.grids[0].name == "g1"
    assert s1.grids[0].capacity == 30

    s1_lp = SystemLP(s1)

    status = s1_lp.solve(keepfiles=False)

    assert status == "ok"

    lp = s1_lp.lp
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[0]) == approx(19.509109)
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[1]) == approx(19.042315)


def test_sbtm_grid_4():
    """Test system_lp 1."""
    ds = """{
      "name": "s1",
      "uid": 1,
      "blocks": [{"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5},
                 {"duration": 0.5}],
      "buses": [{"uid": 1,
                 "name": "home"}],
      "sbtms": [{"name": "home",
                  "uid": 1,
                  "bus_uid": 1,
                  "single_room": {
                      "total_floor_area": 70,
                      "height": 2.5,
                      "u_value": 2,
                      "air_renewal": 0.5,
                      "air_density": 1.225,
                      "air_specific_heat_capacity": 1.005,
                      "thermal_mass_parameter": 250.0,
                      "heating_power": 10,
                      "time_interval": 1800,
                      "initial_temperature": 20,
                      "external_temperatures": 10,
                      "thermal_drift_cost": 5000},
                   "heating_unit": { "capacity": 20, "efficiency": 1.0},
                   "min_temperature": 24
                 }],
      "grids": [{"name": "g1",
                "uid": 1,
                "bus_uid": 1,
                "capacity": 30,
                "energy_tariffs": 150}]
    }"""

    s1: System = System.from_json(ds)

    assert s1.name == "s1"
    assert s1.uid == 1
    assert s1.buses[0].name == "home"
    assert s1.buses[0].uid == 1

    assert s1.sbtms[0].name == "home"

    assert s1.grids[0].name == "g1"
    assert s1.grids[0].capacity == 30

    s1_lp = SystemLP(s1)

    status = s1_lp.solve(keepfiles=True)

    assert status == "ok"

    lp = s1_lp.lp

    assert lp.get_col_at(s1_lp.sbtms_lp[1].onoff_heat_cols[0]) == 1
    assert lp.get_col_at(s1_lp.sbtms_lp[1].onoff_heat_cols[1]) == 1
    assert lp.get_col_at(s1_lp.sbtms_lp[1].onoff_heat_cols[2]) == 1
    assert lp.get_col_at(s1_lp.sbtms_lp[1].onoff_heat_cols[3]) == 1
    assert lp.get_col_at(s1_lp.sbtms_lp[1].onoff_heat_cols[4]) == 0
    assert lp.get_col_at(s1_lp.sbtms_lp[1].onoff_heat_cols[5]) == 0

    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[0]) == approx(21.566252)
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[1]) == approx(23.055618)
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[2]) == approx(24.471872)
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[3]) == approx(25.818604)
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[4]) == approx(25.042083)
    assert lp.get_col_at(s1_lp.sbtms_lp[1].tfin_cols[5]) == approx(24.30368)
