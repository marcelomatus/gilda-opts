"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.grid import Grid
from gilda_opts.grid_sched import GridSched
from gilda_opts.linear_problem import guid


class GridLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, grid: Grid, system_lp=None):
        """Create a GridLP instance.

        Parameters
        ----------
        grid : Grid
            The Grid instance
        system_lp : SystemLP
            The SystemLP where the GridLP will be included
        """
        self.block_withdrawn_cols = {}
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
        lname = guid("gp", uid)
        pmax = self.grid.capacity
        pmax_col = system_lp.lp.add_col(name=lname, lb=0, ub=pmax, c=cvar)
        logging.info("added pmax variable %s %s", lname, pmax_col)
        self.pmax_col = pmax_col

    def add_block(self, index: int, block: Block):
        """Add Grid equations to a block.

        :param index: block index
        :param block: block structure

        """
        bid = index
        uid = self.grid.uid
        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.grid.bus_uid)

        #
        # adding the grid buy (withdrawn) variable
        #
        try:
            energy_cvar = self.grid.energy_tariffs[bid]
        except IndexError:
            energy_cvar = 0

        try:
            emission_cvar = self.grid.emission_factors[bid] * self.grid.emission_cost
        except IndexError:
            emission_cvar = 0

        lname = guid("gb", uid, bid)
        wpmax = self.grid.capacity
        try:
            wpmax *= self.grid.withdrawn_profile[bid]
        except IndexError:
            pass

        cvar = (energy_cvar + emission_cvar) * block.duration

        withdrawn_col = lp.add_col(name=lname, lb=0, ub=wpmax, c=cvar)
        logging.info("added withdrawn variable %s %s", lname, withdrawn_col)

        self.block_withdrawn_cols[bid] = withdrawn_col
        bus_lp.add_block_load_col(bid, withdrawn_col, coeff=-1)

        #
        # adding the grid sell (withdrawn) variable
        #
        try:
            pvar = self.grid.energy_sell_prices[bid] * block.duration
        except IndexError:
            pvar = 0

        if pvar > 0:
            lname = guid("gp", uid, bid)
            ipmax = self.grid.capacity
            try:
                ipmax *= self.grid.withdrawn_profile[bid]
            except IndexError:
                pass

            injection_col = lp.add_col(name=lname, lb=0, ub=ipmax, c=-pvar)
            logging.info("added injection variable %s %s", lname, injection_col)
            self.block_injection_cols[bid] = injection_col
            bus_lp.add_block_load_col(bid, injection_col, coeff=1)

        #
        # adding pmax constraint
        #

        if self.pmax_col < 0:
            return

        row = {}
        try:
            pfact = self.grid.power_factors[bid]
            if pfact > 0:
                row[self.pmax_col] = 1
                row[withdrawn_col] = -pfact
        except IndexError:
            pass

        if len(row) > 1:
            pmax_row = lp.add_row(name=lname, row=row, lb=0)
            logging.info("added pmax constraint %s %s", lname, withdrawn_col)
            self.block_pmax_rows[bid] = pmax_row

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal grid schedule."""
        lp = self.system_lp.lp
        block_withdrawn_values = lp.get_col_sol(self.block_withdrawn_cols.values())
        block_injection_values = lp.get_col_sol(self.block_injection_cols.values())
        return GridSched(
            uid=self.grid.uid,
            name=self.grid.name,
            block_withdrawn_values=block_withdrawn_values,
            block_injection_values=block_injection_values,
        )
