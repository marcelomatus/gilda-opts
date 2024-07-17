"""Contains the demnand_lp class."""

from gilda_opts.bess_lp import BESSLP
from gilda_opts.block import Block
from gilda_opts.electric_car import ATHOME_MASK, ONROAD_MASK, PLUGGED_MASK, ElectricCar
from gilda_opts.electric_car_sched import ElectricCarSched
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.utils import get_number_at


class ElectricCarLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, electric_car: ElectricCar, system_lp=None):
        """Create the ElectricCarLP instance."""
        self.battery_flow_in_cols: dict[int, int] = {}
        self.battery_flow_out_cols: dict[int, int] = {}
        self.battery_efin_cols: dict[int, int] = {}
        self.battery_efin_rows: dict[int, int] = {}
        self.engine_flow_cols: dict[int, int] = {}

        self.electric_car = electric_car
        self.system_lp = system_lp

    def add_block(self, bid: int, block: Block):
        """Add ElectricCar equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        ec: ElectricCar = self.electric_car

        location_mask = get_number_at(ec.location_masks, bid, ATHOME_MASK)
        at_home = location_mask == ATHOME_MASK
        plugged = location_mask == PLUGGED_MASK
        onroad = location_mask == ONROAD_MASK

        bus_uid = (
            ec.athome_bus_uid if at_home else (ec.public_bus_uid if plugged else None)
        )
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
        # engine flow col
        #
        if onroad:
            distance = get_number_at(ec.onroad_distances, bid, 0)
            engine_flow = distance * ec.engine.energy_consumption / block.duration
            lb, ub = engine_flow, engine_flow
        else:
            lb, ub = 0, 0
        cvar = ec.battery.discharge_cost * block.duration
        engine_flow_col = lp.add_col(lb=lb, ub=ub, c=cvar)

        lp.set_coeff(
            battery_efin_row,
            engine_flow_col,
            block.duration / ec.engine.efficiency,
        )

        #
        # save the cols and rows
        #
        self.battery_flow_out_cols[bid] = battery_flow_out_col
        self.battery_flow_in_cols[bid] = battery_flow_in_col
        self.battery_efin_cols[bid] = battery_efin_col
        self.battery_efin_rows[bid] = battery_efin_row
        self.engine_flow_cols[bid] = engine_flow_col

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
        engine_flow_values = lp.get_col_sol(self.engine_flow_cols.values())
        return ElectricCarSched(
            uid=self.electric_car.uid,
            name=self.electric_car.name,
            battery_efin_values=battery_efin_values,
            battery_flow_in_values=battery_flow_in_values,
            battery_flow_out_values=battery_flow_out_values,
            engine_flow_values=engine_flow_values,
        )
