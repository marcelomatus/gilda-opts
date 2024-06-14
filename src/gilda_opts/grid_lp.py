"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.grid import Grid
from gilda_opts.linear_problem import guid
from gilda_opts.grid_sched import GridSched


class GridLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, grid: Grid, system_lp=None):
        """Create the GridLP instance."""
        self.block_injection_cols = {}
        self.block_pmax_rows = {}
        self.pmax_col = -1

        self.grid = grid
        self.system_lp = system_lp

        #
        # Add the pmax variable if needed
        #
        cvar = self.grid.power_tariff
        if cvar <= 0:
            return

        uid = self.grid.uid
        lname = guid('gp', uid)
        pmax = self.grid.capacity
        pmax_col = system_lp.lp.add_col(name=lname, lb=0, ub=pmax, c=cvar)
        logging.info('added pmax variable %s %s' % (lname, pmax_col))
        self.pmax_col = pmax_col

    def add_block(self, block: Block):
        """Add Grid equations to a block."""
        bid = block.index
        uid = self.grid.uid
        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.grid.bus_uid)

        #
        # adding the grid injection  variable
        #
        try:
            energy_cvar = self.grid.energy_tariffs[bid]
        except IndexError:
            energy_cvar = 0

        try:
            emission_cvar = self.grid.emission_factors[bid] * self.emission_cost
        except IndexError:
            emission_cvar = 0

        lname = guid('gb', uid, bid)
        pmax = self.grid.capacity
        cvar = (energy_cvar + emission_cvar) * block.duration

        injection_col = lp.add_col(name=lname, lb=0, ub=pmax, c=cvar)
        logging.info('added injection variable %s %s' % (lname, injection_col))

        self.block_injection_cols[bid] = injection_col
        bus_lp.add_block_load_col(block, injection_col, coeff=-1)

        #
        # adding pmax constraint
        #

        if self.pmax_col < 0:
            return

        try:
            row = {}
            row[self.pmax_col] = 1
            pfact = self.grid.power_factors[bid]
            if pfact > 0:
                row[injection_col] = -pfact
        except IndexError:
            row = {}

        if len(row) > 1:
            pmax_row = lp.add_row(name=lname, row=row, lb=0)
            logging.info('added pmax constraint %s %s' % (lname, injection_col))
            self.block_pmax_rows[bid] = pmax_row

    def get_sched(self):
        """Return the optimal grid schedule."""
        block_injection_values = self.system_lp.lp.get_col_sol(self.block_injection_cols.values())
        return GridSched(uid=self.grid.uid,
                         name=self.grid.name,
                         block_injection_values=block_injection_values)
