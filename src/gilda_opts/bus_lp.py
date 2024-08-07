"""Contains the bus_lp class."""

import numpy as np

from gilda_opts.block import Block
from gilda_opts.bus import Bus
from gilda_opts.bus_sched import BusSched


class BusLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, bus: Bus, system_lp=None):
        """Create the BusLP instance."""
        self.load_rows: dict[int, int] = {}
        self.dual_factors: dict[int, float] = {}

        self.bus = bus
        self.system_lp = system_lp

    def add_block(
        self,
        bid: int,
        block: Block,  # pylint: disable=unused-argument
    ):
        """Add Bus equations to a block."""
        lp = self.system_lp.lp
        row = lp.add_rhs_row(rhs=0)
        self.load_rows[bid] = row
        self.dual_factors[bid] = -block.energy_cost(1)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def add_block_load_col(self, bid, load_col, coeff=1):
        """Add load variable to load row in a block."""
        if coeff == 0:
            return

        i = self.load_rows[bid]
        j = load_col
        self.system_lp.lp.set_coeff(i, j, coeff)

    def get_sched(self):
        """Return bus schedule."""
        lp = self.system_lp.lp
        dual_factors = np.asarray(list(self.dual_factors.values()), dtype=float)
        load_duals = lp.get_dual_sol(self.load_rows.values()) / dual_factors

        return BusSched(
            uid=self.bus.uid,
            name=self.bus.name,
            load_duals=load_duals,
        )
