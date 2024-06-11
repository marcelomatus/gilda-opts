"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.demand import Demand
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

    def add_block(self, block: Block):
        """Add Demand equations to a block."""
        bid = block.index
        uid = self.demand.uid
        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.demand.bus_uid)

        row = {}
        #
        # adding the load variable
        #
        lname = guid('lb', uid, bid)
        load = self.demand.loads[bid]
        load_col = lp.add_col(name=lname, lb=0, ub=load, c=0)
        logging.info('added load variable %s %s' % (lname, load_col))

        self.block_load_cols[bid] = load_col
        bus_lp.add_block_load_col(block, load_col)

        #
        # adding the fail
        #
        cfail = self.demand.cfail
        cfail *= block.duration * block.discount

        if cfail <= 0.0:
            return

        fname = guid('df', uid, bid)
        fail_col = lp.add_col(name=fname, lb=0, c=cfail)
        logging.info('added fail variable %s %s' % (fname, fail_col))
        self.block_fail_cols[bid] = fail_col

        row = {}
        row[load_col] = 1
        row[fail_col] = 1

        load_row = lp.add_rhs_row(name=lname, rhs=load, row=row)
        self.block_load_rows[bid] = load_row
        logging.info('added load + fail row %s %s' % (lname, load_row))
