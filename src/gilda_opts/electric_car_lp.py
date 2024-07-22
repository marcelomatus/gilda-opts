"""Contains the demnand_lp class."""

import numpy as np

from gilda_opts.bess_lp import BESSLP
from gilda_opts.block import Block
from gilda_opts.electric_car import ElectricCar
from gilda_opts.electric_car_sched import ElectricCarSched
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.utils import get_value_at


class ElectricCarLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, electric_car: ElectricCar, system_lp=None):
        """Create the ElectricCarLP instance."""
        self.battery_flow_in_cols: dict[int, int] = {}
        self.battery_flow_out_cols: dict[int, int] = {}
        self.battery_efin_cols: dict[int, int] = {}
        self.battery_efin_rows: dict[int, int] = {}
        self.engine_distance_cols: dict[int, int] = {}
        self.engine_distance_rows: dict[int, int] = {}
        self.dual_factors: dict[int, float] = {}

        self.electric_car = electric_car
        self.system_lp = system_lp

    def add_block(self, bid: int, block: Block):
        """Add ElectricCar equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        ec: ElectricCar = self.electric_car

        self.dual_factors[bid] = block.energy_cost(1)

        bus_uid = get_value_at(ec.bus_uid_sched, bid, -1)
        onroad = bus_uid < 0
        bus_lp = self.system_lp.get_bus_lp(bus_uid) if not onroad else None

        prev_efin_col = self.battery_efin_cols[bid - 1] if bid > 0 else -1

        (
            battery_flow_in_col,
            battery_flow_out_col,
            battery_efin_col,
            battery_efin_row,
        ) = BESSLP.add_block_i(
            lp=lp,
            bid=bid,
            block=block,
            prev_efin_col=prev_efin_col,
            bess=ec.battery,
            bus_lp=bus_lp,
        )

        #
        # engine distance col
        #
        distance = get_value_at(ec.distance_sched, bid, 0) if onroad else -1
        if distance > 0:
            row = {}

            cfail_sched = get_value_at(ec.cfail_sched, bid, -1)
            cfail = block.energy_cost(cfail_sched)

            #
            # add engine_distance_col
            #
            ub = distance
            lb = 0 if cfail > 0.0 else ub

            dist_to_kwh = 1.0 / (
                ec.battery.efficiency_out * ec.engine.energy_efficiency
            )

            ceng = block.power_cost(ec.battery.discharge_cost * dist_to_kwh)
            engine_distance_col = lp.add_col(lb=lb, ub=ub, c=ceng)

            self.engine_distance_cols[bid] = engine_distance_col
            #
            # add the engine flow to the battery balance row
            #
            lp.set_coeff(battery_efin_row, engine_distance_col, dist_to_kwh)

            row[engine_distance_col] = 1

            #
            # adding the distance fail variable
            #
            if cfail > 0.0:
                distance_fail_col = lp.add_col(lb=0, ub=distance, c=cfail)
                row[distance_fail_col] = 1

            engine_distance_row = lp.add_row(row, lb=distance)
        else:
            engine_distance_col = -1
            engine_distance_row = -1

        #
        # save the cols and rows
        #
        self.battery_flow_out_cols[bid] = battery_flow_out_col
        self.battery_flow_in_cols[bid] = battery_flow_in_col
        self.battery_efin_cols[bid] = battery_efin_col
        self.battery_efin_rows[bid] = battery_efin_row
        self.engine_distance_cols[bid] = engine_distance_col
        self.engine_distance_rows[bid] = engine_distance_row

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        BESSLP.post_blocks_i(
            self.system_lp.lp, self.battery_efin_cols, self.electric_car.battery
        )

    def get_sched(self):
        """Return the optimal electric_car schedule."""
        lp = self.system_lp.lp
        battery_efin_values = lp.get_col_sol(self.battery_efin_cols.values())
        battery_flow_in_values = lp.get_col_sol(self.battery_flow_in_cols.values())
        battery_flow_out_values = lp.get_col_sol(self.battery_flow_out_cols.values())
        engine_distance_values = lp.get_col_sol(self.engine_distance_cols.values(), 0)

        dual_factors = np.asarray(list(self.dual_factors.values()), dtype=float)
        engine_distance_duals = (
            lp.get_dual_sol(self.engine_distance_rows.values(), 0) / dual_factors
        )

        return ElectricCarSched(
            uid=self.electric_car.uid,
            name=self.electric_car.name,
            battery_efin_values=battery_efin_values,
            battery_flow_in_values=battery_flow_in_values,
            battery_flow_out_values=battery_flow_out_values,
            engine_distance_values=engine_distance_values,
            engine_distance_duals=engine_distance_duals,
        )
