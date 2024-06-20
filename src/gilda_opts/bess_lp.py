"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem, guid
from gilda_opts.bess import BESS
from gilda_opts.bess_sched import BESSSched


class BESSLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, bess: BESS, system_lp=None):
        """Create the BESSLP instance."""
        self.block_inflow_cols = {}
        self.block_outflow_cols = {}
        self.block_efin_cols = {}
        self.block_efin_rows = {}

        self.bess = bess
        self.system_lp = system_lp

    def add_block(self, index: int, block: Block):
        """Add BESS equations to a block."""
        bid = index
        uid = self.bess.uid
        lp : LinearProblem = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.bess.bus_uid)
        max_flow = self.bess.max_flow
        efficiency = self.bess.efficiency

        #
        # inflow col
        #
        lname = guid('bi', uid, bid)
        inflow_col = lp.add_col(name=lname, lb=0, ub=max_flow)
        logging.info('added inflow variable %s %d' % (lname, inflow_col))
        self.block_inflow_cols[bid] = inflow_col
        bus_lp.add_block_load_col(bid, inflow_col, coeff=+1.0)

        #
        # outflow col
        #
        lname = guid('bo', uid, bid)
        outflow_col = lp.add_col(name=lname, lb=0, ub=max_flow)
        logging.info('added outflow variable %s %d' % (lname, outflow_col))
        self.block_outflow_cols[bid] = outflow_col
        bus_lp.add_block_load_col(bid, outflow_col, coeff=-1.0)

        #
        # efin col
        #
        lname = guid('be', uid, bid)
        capacity = self.bess.capacity
        efin_col = lp.add_col(name=lname, lb=0, ub=capacity)
        logging.info('added efin variable %s %d' % (lname, efin_col))
        self.block_efin_cols[bid] = efin_col

        #
        # efin row
        #
        row = {}
        row[efin_col] = 1
        row[inflow_col] = -block.duration * efficiency
        row[outflow_col] = block.duration / efficiency

        if bid == 0:
            lb = self.bess.eini
            ub = self.bess.eini
        else:
            lb = 0
            ub = 0
            row[self.block_efin_cols[bid - 1]] = -1

        lname = guid('br', uid, bid)
        efin_row = lp.add_row(row, name=lname, lb=lb, ub=ub)
        logging.info('added efin row %s %d' % (lname, efin_row))
        self.block_efin_rows[bid] = efin_row

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        pass

    def get_sched(self):
        """Return the optimal bess schedule."""
        lp = self.system_lp.lp
        block_efin_values = lp.get_col_sol(self.block_efin_cols.values())
        block_inflow_values = lp.get_col_sol(self.block_inflow_cols.values())
        block_outflow_values = lp.get_col_sol(self.block_outflow_cols.values())
        return BESSSched(uid=self.bess.uid,
                         name=self.bess.name,
                         block_efin_values=block_efin_values,
                         block_inflow_values=block_inflow_values,
                         block_outflow_values=block_outflow_values
                         )
