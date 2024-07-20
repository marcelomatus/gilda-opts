"""Contains the demnand_lp class."""

import logging
from gilda_opts.sbtm import SingleRoom, ThermalUnit, SBTM
from gilda_opts.sbtm_sched import SBTMSched
from gilda_opts.block import Block
from gilda_opts.bus_lp import BusLP
from gilda_opts.linear_problem import LinearProblem, guid
from gilda_opts.utils import get_value_at, NumberSched


class SBTMLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, sbtm: SBTM, system_lp=None):
        """Create the SBTMLP instance."""
        self.onoff_heat_cols: dict[int, int] = {}
        self.onoff_cool_cols: dict[int, int] = {}
        self.tfin_cols: dict[int, int] = {}

        self.sbtm = sbtm
        self.system_lp = system_lp

    @staticmethod
    def add_thermal_unit(
        lp: LinearProblem,
        bid: int,
        block: Block,
        single_room: SingleRoom,
        thermal_unit: ThermalUnit,
        heat_direction: int,
        reference_temperature: NumberSched,
        tfin_col: int,
    ):
        """Add thermal unit control.

        heat_direction: 1 or -1, heating or cooling
        """
        #
        # onoff_q col
        #
        inf = float("inf")

        D_t = block.duration * 3600  # pylint: disable=C0103
        q_coeff = heat_direction * D_t * single_room.q_coeff(thermal_unit)

        tcost = block.duration * get_value_at(single_room.thermal_drift_cost, bid, 0)

        if q_coeff * tcost != 0:
            onoff_col = lp.add_col(lb=0, ub=1, ctype=1)

            ep_col = lp.add_col(lb=0, ub=inf, c=tcost)
            en_col = lp.add_col(lb=0, ub=inf, c=0)

            tref = get_value_at(
                reference_temperature, bid, single_room.initial_temperature
            )

            row = {}
            row[tfin_col] = heat_direction
            row[ep_col] = 1
            row[en_col] = -1
            lb = ub = heat_direction * tref

            lp.add_row(row, lb=lb, ub=ub)
        else:
            onoff_col = ep_col = -1

        return onoff_col, q_coeff

    @staticmethod
    def add_block_i(
        lp: LinearProblem,
        bid: int,
        block: Block,
        prev_tfin_col: int,
        sbtm: SBTM,
        bus_lp: BusLP,
    ):
        """Adding the block constraints to the LP.

        :param lp:
        :param bid:
        :param block:
        :param prev_efin_col:
        :param sbtm:
        :returns: the col and row indexes
        """
        single_room = sbtm.single_room
        heating_unit = sbtm.heating_unit
        cooling_unit = sbtm.cooling_unit
        min_temperature = sbtm.min_temperature
        max_temperature = sbtm.max_temperature

        D_t = block.duration * 3600  # pylint: disable=C0103
        t_coeff = D_t * single_room.temperature_coeff()

        #
        # tfin col
        #
        lb, ub = 0, 50
        tfin_col = lp.add_col(lb=lb, ub=ub)

        tini = single_room.initial_temperature
        text = get_value_at(single_room.external_temperatures, bid, tini)

        row: dict[int, float] = {}
        row[tfin_col] = 1

        #
        # heating col
        #
        heating_col, heating_coeff = SBTMLP.add_thermal_unit(
            lp=lp,
            bid=bid,
            block=block,
            single_room=single_room,
            thermal_unit=heating_unit,
            heat_direction=1,
            reference_temperature=min_temperature,
            tfin_col=tfin_col,
        )

        if heating_col >= 0:
            bus_lp.add_block_load_col(bid, heating_col, coeff=heating_unit.capacity)
            row[heating_col] = -heating_coeff

        #
        # cooling col
        #
        cooling_col, cooling_coeff = SBTMLP.add_thermal_unit(
            lp=lp,
            bid=bid,
            block=block,
            single_room=single_room,
            thermal_unit=cooling_unit,
            heat_direction=1,
            reference_temperature=max_temperature,
            tfin_col=tfin_col,
        )

        if cooling_col >= 0:
            bus_lp.add_block_load_col(bid, cooling_col, coeff=cooling_unit.capacity)
            row[cooling_col] = -cooling_coeff

        #
        # tfin row
        #
        if prev_tfin_col >= 0:
            ub = lb = t_coeff * text
            row[prev_tfin_col] = -1 + t_coeff
        else:
            ub = lb = tini * (1 - t_coeff) + t_coeff * text
        tfin_row = lp.add_row(row, lb=lb, ub=ub)

        return heating_col, cooling_col, tfin_col, tfin_row

    def add_block(self, index: int, block: Block):
        """Add SBTM equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        bid = index
        bus_lp = self.system_lp.get_bus_lp(self.sbtm.bus_uid)
        prev_tfin_col = self.tfin_cols[bid - 1] if bid > 0 else -1

        (onoff_heat_col, onoff_cool_col, tfin_col, tfin_row) = SBTMLP.add_block_i(
            lp=lp,
            bid=bid,
            block=block,
            prev_tfin_col=prev_tfin_col,
            sbtm=self.sbtm,
            bus_lp=bus_lp,
        )

        self.onoff_heat_cols[bid] = onoff_heat_col
        self.onoff_cool_cols[bid] = onoff_cool_col
        self.tfin_cols[bid] = tfin_col

        uid = self.sbtm.uid
        lname = guid("sbtm", uid, bid)
        logging.info("added onoff_heat variable %s %d", lname, onoff_heat_col)
        logging.info("added onoff_cool variable %s %d", lname, onoff_cool_col)
        logging.info("added tfin variable %s %d", lname, tfin_col)
        logging.info("added tfin row %s %d", lname, tfin_row)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal sbtm schedule."""
        lp = self.system_lp.lp
        tfin_values = lp.get_col_sol(self.tfin_cols.values())
        onoff_heat_values = lp.get_col_sol(self.onoff_heat_cols.values())
        onoff_cool_values = lp.get_col_sol(self.onoff_cool_cols.values())
        return SBTMSched(
            uid=self.sbtm.uid,
            name=self.sbtm.name,
            tfin_values=tfin_values,
            onoff_heat_values=onoff_heat_values,
            onoff_cool_values=onoff_cool_values,
        )
