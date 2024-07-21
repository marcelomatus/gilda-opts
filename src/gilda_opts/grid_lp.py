"""Contains the demnand_lp class."""

from gilda_opts.block import Block
from gilda_opts.grid import Grid
from gilda_opts.grid_sched import GridSched
from gilda_opts.utils import get_value_at


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
        self.withdrawn_cols: dict[int, int] = {}
        self.injection_cols: dict[int, int] = {}
        self.pmax_rows: dict[int, int] = {}
        self.pmax_col = -1

        self.grid = grid
        self.system_lp = system_lp

        #
        # Add the pmax variable if needed
        #
        cvar = self.grid.power_tariff
        if cvar <= 0:
            return

        pmax = self.grid.capacity
        pmax_col = system_lp.lp.add_col(lb=0, ub=pmax, c=cvar)

        self.pmax_col = pmax_col

    def add_block(self, bid: int, block: Block):
        """Add Grid equations to a block.

        :param bid: block index
        :param block: block structure

        """
        grid = self.grid

        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(grid.bus_uid)

        #
        # adding the grid buy (withdrawn) variable
        #
        energy_cvar = get_value_at(grid.energy_buy_price_sched, bid, 0)
        emission_factor = get_value_at(grid.emission_factor_sched, bid, 0)
        emission_cvar = grid.emission_cost * emission_factor
        cvar = block.energy_cost(energy_cvar + emission_cvar)

        wpmax = grid.capacity * get_value_at(grid.withdrawn_profile_sched, bid, 1)
        withdrawn_col = lp.add_col(lb=0, ub=wpmax, c=cvar)

        self.withdrawn_cols[bid] = withdrawn_col
        bus_lp.add_block_load_col(bid, withdrawn_col, coeff=-1)

        #
        # adding the grid sell (injection) variable
        #
        pvar = block.energy_cost(get_value_at(grid.energy_sell_price_sched, bid, 0))

        if pvar > 0:
            ipmax = grid.capacity * get_value_at(grid.injection_profile_sched, bid, 1)
            injection_col = lp.add_col(lb=0, ub=ipmax, c=-pvar)
            self.injection_cols[bid] = injection_col
            bus_lp.add_block_load_col(bid, injection_col, coeff=1)

        #
        # adding pmax constraint
        #
        pfact = get_value_at(grid.power_factor_sched, bid, 0)
        if self.pmax_col >= 0 and pfact > 0:
            row = {}
            row[self.pmax_col] = 1
            row[withdrawn_col] = -pfact

            pmax_row = lp.add_row(row=row, lb=0)
            self.pmax_rows[bid] = pmax_row

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal grid schedule."""
        lp = self.system_lp.lp
        withdrawn_values = lp.get_col_sol(self.withdrawn_cols.values())
        injection_values = lp.get_col_sol(self.injection_cols.values())
        return GridSched(
            uid=self.grid.uid,
            name=self.grid.name,
            withdrawn_values=withdrawn_values,
            injection_values=injection_values,
        )
