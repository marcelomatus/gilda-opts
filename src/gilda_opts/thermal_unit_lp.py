"""Contains the srts_lp class."""

from gilda_opts.single_room import SingleRoom
from gilda_opts.thermal_unit import ThermalUnit
from gilda_opts.srts import SRTS, MAX_TEMPERATURE, MIN_TEMPERATURE
from gilda_opts.thermal_unit_sched import ThermalUnitSched
from gilda_opts.block import Block
from gilda_opts.bus_lp import BusLP
from gilda_opts.srts_lp import SRTSLP
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.utils import get_value_at

MAX_TEMPERATURE_RANGE = MAX_TEMPERATURE - MIN_TEMPERATURE


class ThermalUnitLP:
    """Represents a Thermal Unit in the LP formulation."""

    def __init__(self, thermal_unit: ThermalUnit, system_lp=None):
        """Create the ThermalUnit instance."""
        self.onoff_cols: dict[int, int] = {}
        self.onoff_rows: dict[int, int] = {}

        self.thermal_unit = thermal_unit
        self.system_lp = system_lp

    @staticmethod
    def add_block_i(
        lp: LinearProblem,
        bid: int,
        block: Block,
        srts: SRTS,
        thermal_unit: ThermalUnit,
        srts_lp: SRTSLP,
    ):
        """Add thermal unit constraints to block."""
        #
        # onoff_q col
        #
        single_room: SingleRoom = srts.single_room

        (thermal_capacity, thermal_cost_sched, heat_direction) = (
            thermal_unit.get_thermal_capacity(bid)
        )

        q_coeff = heat_direction * single_room.q_coeff(block.duration, thermal_capacity)

        if q_coeff != 0:
            tcost = block.energy_cost(thermal_cost_sched)
            ctype = block.intvar_type
            onoff_col = lp.add_col(lb=0, ub=1, c=tcost, ctype=ctype)
            srts_lp.add_block_q_col(bid, onoff_col, q_coeff)

            epcost = block.energy_cost(
                get_value_at(srts.thermal_drift_cost_sched, bid, 0)
            )
            ep_col = lp.add_col(ub=MAX_TEMPERATURE_RANGE, c=epcost)
            en_col = lp.add_col(ub=MAX_TEMPERATURE_RANGE, c=0)

            tref_sched = (
                srts.min_temperature_sched
                if heat_direction > 0
                else srts.max_temperature_sched
            )
            tref = get_value_at(tref_sched, bid, single_room.initial_temperature)

            row = {}
            tfin_col = srts_lp.get_tfin_col(bid)
            row[tfin_col] = heat_direction
            row[ep_col] = 1
            row[en_col] = -1
            lb = ub = heat_direction * tref
            onoff_row = lp.add_row(row, lb=lb, ub=ub)

        else:
            onoff_col = -1  # lp.add_col(lb=0, ub=1, c=1)
            onoff_row = -1

        return onoff_col, onoff_row

    def add_block(self, bid: int, block: Block):
        """Add thermal units equation to a block."""
        lp: LinearProblem = self.system_lp.lp
        srts_lp: SRTSLP = self.system_lp.get_srts_lp(self.thermal_unit.srts_uid)

        onoff_col, onoff_row = ThermalUnitLP.add_block_i(
            lp=lp,
            bid=bid,
            block=block,
            srts=srts_lp.srts,
            thermal_unit=self.thermal_unit,
            srts_lp=srts_lp,
        )

        bus_id = self.thermal_unit.bus_uid
        if bus_id >= 0 and onoff_row >= 0:
            bus_lp: BusLP = self.system_lp.get_bus_lp(bus_id)
            bus_lp.add_block_load_col(bid, onoff_col, coeff=self.thermal_unit.capacity)

        self.onoff_cols[bid], self.onoff_rows[bid] = onoff_col, onoff_row

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal thermal_unit schedule."""
        lp = self.system_lp.lp
        onoff_values = lp.get_col_sol(self.onoff_cols.values(), def_value=0)
        return ThermalUnitSched(
            uid=self.thermal_unit.uid,
            name=self.thermal_unit.name,
            onoff_values=onoff_values,
        )
