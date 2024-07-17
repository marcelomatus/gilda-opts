"""Contains the bus_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.bus import Bus
from gilda_opts.linear_problem import guid


class BusLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, bus: Bus, system_lp=None):
        """Create the BusLP instance."""
        self.load_rows: dict[int, int] = {}

        self.bus = bus
        self.system_lp = system_lp

    def add_block(self, index: int, block: Block):  # pylint: disable=unused-argument
        """Add Bus equations to a block."""
        bid = index
        uid = self.bus.uid
        name = guid("lb", uid, bid)
        lp = self.system_lp.lp
        row = lp.add_rhs_row(name=name, rhs=0)
        self.load_rows[bid] = row

        logging.info("added block load balance row %s %s", name, row)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def add_block_load_col(self, index, load_col, coeff=1):
        """Add load variable to load row in a block."""
        i = self.load_rows[index]
        j = load_col
        self.system_lp.lp.set_coeff(i, j, coeff)
