"""Contains the demnand_lp class."""

from gilda_opts.bess import BESS
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
        self.battery_inflow_cols = {}
        self.battery_outflow_cols = {}
        self.battery_efin_cols = {}
        self.battery_efin_rows = {}
        self.engine_flow_cols = {}

        self.electric_car = electric_car
        self.system_lp = system_lp

        ec: ElectricCar = electric_car

        discharge_cost = ec.battery_replacement_cost / ec.battery_cycle_life
        self.bess = BESS(
            max_flow=ec.battery_max_flow,
            efficiency=ec.battery_efficiency,
            capacity=ec.battery_capacity,
            eini=ec.battery_initial_charge,
            efin=ec.battery_final_charge,
            discharge_cost=discharge_cost,
        )

    def add_block(self, index: int, block: Block):
        """Add ElectricCar equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        ec: ElectricCar = self.electric_car
        bid = index
        lp: LinearProblem = self.system_lp.lp

        location_mask = get_number_at(ec.location_masks, bid, ATHOME_MASK)
        at_home = location_mask == ATHOME_MASK
        plugged = location_mask == PLUGGED_MASK
        onroad = location_mask == ONROAD_MASK

        bus_uid = (
            ec.athome_bus_uid if at_home else (ec.charger_bus_uid if plugged else None)
        )
        bus_lp = self.system_lp.get_bus_lp(bus_uid) if not onroad else None

        prev_efin_col = self.battery_efin_cols[bid - 1] if bid > 0 else -1

        (
            battery_inflow_col,
            battery_outflow_col,
            battery_efin_col,
            battery_efin_row,
        ) = BESSLP.add_block_i(
            lp=lp,
            bid=bid,
            block=block,
            prev_efin_col=prev_efin_col,
            bess=self.bess,
            bus_lp=bus_lp,
        )

        #
        # engine flow col
        #
        distance = get_number_at(ec.onroad_distances, bid, 0)
        engine_flow = distance * ec.energy_consumption / block.duration
        if bus_lp is None:
            lb, ub = engine_flow, engine_flow
        else:
            lb, ub = 0, 0
        cvar = self.bess.discharge_cost * block.duration
        engine_flow_col = lp.add_col(lb=lb, ub=ub, c=cvar)

        lp.set_coeff(
            battery_efin_row, engine_flow_col, block.duration / self.bess.efficiency
        )

        #
        # save the cols and rows
        #
        self.battery_outflow_cols[bid] = battery_outflow_col
        self.battery_inflow_cols[bid] = battery_inflow_col
        self.battery_efin_cols[bid] = battery_efin_col
        self.battery_efin_rows[bid] = battery_efin_row
        self.engine_flow_cols[bid] = engine_flow_col

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        BESSLP.post_blocks_i(self.system_lp.lp, self.battery_efin_cols, self.bess)

    def get_sched(self):
        """Return the optimal electric_car schedule."""
        lp = self.system_lp.lp
        battery_efin_values = lp.get_col_sol(self.battery_efin_cols.values())
        battery_inflow_values = lp.get_col_sol(self.battery_inflow_cols.values())
        battery_outflow_values = lp.get_col_sol(self.battery_outflow_cols.values())
        engine_flow_values = lp.get_col_sol(self.engine_flow_cols.values())
        return ElectricCarSched(
            uid=self.electric_car.uid,
            name=self.electric_car.name,
            block_battery_efin_values=battery_efin_values,
            block_battery_inflow_values=battery_inflow_values,
            block_battery_outflow_values=battery_outflow_values,
            block_engine_flow_values=engine_flow_values,
        )
