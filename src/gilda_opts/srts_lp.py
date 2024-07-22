"""Contains the srts_lp class."""

import numpy as np

from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.srts import MAX_TEMPERATURE, MIN_TEMPERATURE, SRTS
from gilda_opts.srts_sched import SRTSSched
from gilda_opts.utils import get_value_at


class SRTSLP:
    """Represents a SRTS in the LP formulation."""

    def __init__(self, srts: SRTS, system_lp=None):
        """Create the SRTSLP instance."""
        self.tfin_cols: dict[int, int] = {}
        self.tfin_rows: dict[int, int] = {}
        self.dual_factors: dict[int, float] = {}

        self.srts = srts
        self.system_lp = system_lp

    @staticmethod
    def add_block_i(
        lp: LinearProblem,
        bid: int,
        block: Block,
        prev_tfin_col: int,
        srts: SRTS,
    ):
        """Adding the block constraints to the LP."""
        single_room = srts.single_room
        t_coeff = single_room.temperature_coeff(block.duration)

        #
        # tfin col
        #
        lb, ub = MIN_TEMPERATURE, MAX_TEMPERATURE
        tfin_col = lp.add_col(lb=lb, ub=ub)

        tini = single_room.initial_temperature
        text = get_value_at(single_room.external_temperature_sched, bid, tini)

        qext = single_room.q_coeff(
            block.duration, get_value_at(single_room.external_heating_sched, bid, 0)
        )

        #
        # tfin row
        #
        row = {}
        row[tfin_col] = 1

        if prev_tfin_col >= 0:
            ub = lb = t_coeff * text + qext
            row[prev_tfin_col] = -1 + t_coeff
        else:
            ub = lb = tini * (1 - t_coeff) + t_coeff * text + qext
        tfin_row = lp.add_row(row, lb=lb, ub=ub)

        return tfin_col, tfin_row

    def add_block(self, bid: int, block: Block):
        """Add SRTS equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        prev_tfin_col = self.tfin_cols[bid - 1] if bid > 0 else -1

        tfin_col, tfin_row = SRTSLP.add_block_i(
            lp=lp,
            bid=bid,
            block=block,
            prev_tfin_col=prev_tfin_col,
            srts=self.srts,
        )

        self.tfin_cols[bid], self.tfin_rows[bid] = tfin_col, tfin_row
        self.dual_factors[bid] = -block.energy_cost(1)

    def get_tfin_col(self, bid: int):
        """Return tfin col and row."""
        return self.tfin_cols[bid]

    def add_block_q_col(self, bid, q_col, q_coeff):
        """Add a heat flow to the room temperature."""
        if q_coeff == 0:
            return

        lp: LinearProblem = self.system_lp.lp
        lp.set_coeff(self.tfin_rows[bid], q_col, -q_coeff)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal srts schedule."""
        lp = self.system_lp.lp
        dual_factors = np.asarray(list(self.dual_factors.values()), dtype=float)
        tfin_duals = lp.get_dual_sol(self.tfin_rows.values()) / dual_factors

        tfin_values = lp.get_col_sol(self.tfin_cols.values())

        return SRTSSched(
            uid=self.srts.uid,
            name=self.srts.name,
            tfin_duals=tfin_duals,
            tfin_values=tfin_values,
        )
