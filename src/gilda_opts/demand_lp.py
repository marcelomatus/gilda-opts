"""Contains the demnand_lp class."""

from gilda_opts.block import Block
from gilda_opts.demand import Demand
from gilda_opts.demand_sched import DemandSched
from gilda_opts.utils import get_value_at


class DemandLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, demand: Demand, system_lp=None):
        """Create the DemandLP instance."""
        self.load_cols: dict[int, int] = {}
        self.fail_cols: dict[int, int] = {}
        self.fail_rows: dict[int, int] = {}

        self.demand = demand
        self.system_lp = system_lp

    def add_block(self, bid: int, block: Block):
        """Add Demand equations to a block."""
        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.demand.bus_uid)

        #
        # adding the load variable
        #
        cfail_sched = get_value_at(self.demand.cfail_sched, bid, -1)
        cfail = block.energy_cost(cfail_sched)

        load = get_value_at(self.demand.load_sched, bid, 0)
        ub = load
        lb = 0 if cfail > 0.0 else ub
        load_col = lp.add_col(lb=lb, ub=ub, c=0)

        self.load_cols[bid] = load_col
        bus_lp.add_block_load_col(bid, load_col)

        #
        # adding the fail variable
        #
        if cfail <= 0.0:
            return

        fail_col = lp.add_col(lb=0, ub=load, c=cfail)
        self.fail_cols[bid] = fail_col

        row = {}
        row[load_col] = 1
        row[fail_col] = 1

        fail_row = lp.add_row(row=row, lb=load)
        self.fail_rows[bid] = fail_row

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal demand schedule."""
        lp = self.system_lp.lp
        load_values = lp.get_col_sol(self.load_cols.values())
        fail_values = lp.get_col_sol(self.fail_cols.values())
        return DemandSched(
            uid=self.demand.uid,
            name=self.demand.name,
            load_values=load_values,
            fail_values=fail_values,
        )
