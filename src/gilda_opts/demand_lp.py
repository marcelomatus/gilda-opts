"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.demand import Demand
from gilda_opts.demand_sched import DemandSched
from gilda_opts.linear_problem import guid


class DemandLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, demand: Demand, system_lp=None):
        """Create the DemandLP instance."""
        self.block_load_cols = {}
        self.block_fail_cols = {}
        self.block_load_rows = {}

        self.demand = demand
        self.system_lp = system_lp

    def add_block(self, index: int, block: Block):
        """Add Demand equations to a block."""
        bid = index
        uid = self.demand.uid
        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.demand.bus_uid)

        row = {}
        #
        # adding the load variable
        #
        cfail = self.demand.cfail
        cfail *= block.duration * block.discount

        lname = guid("lb", uid, bid)
        ub = self.demand.loads[bid]
        lb = 0 if cfail > 0 else ub
        load_col = lp.add_col(name=lname, lb=lb, ub=ub, c=0)
        logging.info("added load variable %s %s", lname, load_col)

        self.block_load_cols[bid] = load_col
        bus_lp.add_block_load_col(bid, load_col)

        #
        # adding the fail variable
        #
        if cfail <= 0.0:
            return

        fname = guid("df", uid, bid)
        fail_col = lp.add_col(name=fname, lb=0, c=cfail)
        logging.info("added fail variable %s %s", fname, fail_col)
        self.block_fail_cols[bid] = fail_col

        row = {}
        row[load_col] = 1
        row[fail_col] = 1

        load_row = lp.add_rhs_row(name=lname, rhs=ub, row=row)
        self.block_load_rows[bid] = load_row
        logging.info("added load + fail row %s %s", lname, load_row)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal demand schedule."""
        lp = self.system_lp.lp
        block_load_values = lp.get_col_sol(self.block_load_cols.values())
        block_fail_values = lp.get_col_sol(self.block_fail_cols.values())
        return DemandSched(
            uid=self.demand.uid,
            name=self.demand.name,
            block_load_values=block_load_values,
            block_fail_values=block_fail_values,
        )
