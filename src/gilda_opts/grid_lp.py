"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.grid import Grid
from gilda_opts.linear_problem import guid


class GridLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, grid: Grid, system_lp=None):
        """Create the GridLP instance."""
        self.block_injection_cols = {}
        self.grid = grid
        self.system_lp = system_lp

    def add_block(self, block: Block):
        """Add Grid equations to a block."""
        bid = block.index
        uid = self.grid.uid
        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.grid.bus_uid)

        #
        # adding the grid injection  variable
        #
        lname = guid('ib', uid, bid)
        pmax = self.grid.capacity
        injection_col = lp.add_col(name=lname, lb=0, ub=pmax, c=0)
        logging.info('added injection variable %s %s' % (lname, injection_col))

        self.block_injection_cols[bid] = injection_col
        bus_lp.add_block_load_col(block, injection_col, coeff=-1)
