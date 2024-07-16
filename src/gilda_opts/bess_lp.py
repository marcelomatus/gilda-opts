"""Contains the demnand_lp class."""

import logging

from gilda_opts.bus_lp import BusLP
from gilda_opts.bess import BESS
from gilda_opts.bess_sched import BESSSched
from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem, guid


class BESSLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, bess: BESS, system_lp=None):
        """Create the BESSLP instance."""
        self.inflow_cols = {}
        self.outflow_cols = {}
        self.efin_cols = {}
        self.efin_rows = {}

        self.bess = bess
        self.system_lp = system_lp

    @staticmethod
    def add_block_i(
        lp: LinearProblem,
        bid: int,
        block: Block,
        prev_efin_col: int,
        bess: BESS,
        bus_lp: BusLP = None,
    ):
        """Adding the block constraints to the LP.

        :param lp:
        :param bid:
        :param block:
        :param prev_efin_col:
        :param bess:
        :param bus_lp:
        :returns: the col and row indexes
        """
        max_flow = bess.max_flow
        efficiency = bess.efficiency
        capacity = bess.capacity
        eini = bess.eini
        efin = bess.efin
        discharge_cost = bess.discharge_cost

        #
        # inflow col
        #
        inflow_col = lp.add_col(lb=0, ub=max_flow)

        #
        # outflow col
        #
        cvar = discharge_cost * block.duration
        outflow_col = lp.add_col(lb=0, ub=max_flow, c=cvar)

        #
        # adding the flows to the bus
        #
        if bus_lp is not None:
            bus_lp.add_block_load_col(bid, inflow_col, coeff=+1.0)
            bus_lp.add_block_load_col(bid, outflow_col, coeff=-1.0)

        #
        # efin col
        #
        efin_col = lp.add_col(lb=efin, ub=capacity)

        #
        # efin row
        #
        row = {}
        row[efin_col] = 1
        row[inflow_col] = -block.duration * efficiency
        row[outflow_col] = block.duration / efficiency

        if prev_efin_col < 0:
            lb, ub = eini, eini
        else:
            lb, ub = 0, 0
            row[prev_efin_col] = -1

        efin_row = lp.add_row(row, lb=lb, ub=ub)

        return inflow_col, outflow_col, efin_col, efin_row

    def add_block(self, index: int, block: Block):
        """Add BESS equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        bid = index
        bus_lp = self.system_lp.get_bus_lp(self.bess.bus_uid)
        prev_efin_col = self.efin_cols[bid - 1] if bid > 0 else -1

        inflow_col, outflow_col, efin_col, efin_row = BESSLP.add_block_i(
            lp=lp,
            bid=bid,
            block=block,
            prev_efin_col=prev_efin_col,
            bess=self.bess,
            bus_lp=bus_lp,
        )

        self.outflow_cols[bid] = outflow_col
        self.inflow_cols[bid] = inflow_col
        self.efin_cols[bid] = efin_col
        self.efin_rows[bid] = efin_row

        uid = self.bess.uid
        lname = guid("bess", uid, bid)
        logging.info("added inflow variable %s %d", lname, inflow_col)
        logging.info("added outflow variable %s %d", lname, outflow_col)
        logging.info("added efin variable %s %d", lname, efin_col)
        logging.info("added efin row %s %d", lname, efin_row)

    @staticmethod
    def post_blocks_i(
        lp: LinearProblem,
        efin_cols,
        bess,
    ):
        """Close the LP formulation post the blocks formulation."""
        #
        # Set the efin value, or negative cost
        #
        ncols = len(efin_cols)
        if ncols > 0:
            efin_col = efin_cols[ncols - 1]
            lp.set_col_lb(efin_col, bess.efin)
            lp.set_objc(efin_col, -bess.efin_price)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        BESSLP.post_blocks_i(self.system_lp.lp, self.efin_cols, self.bess)

    def get_sched(self):
        """Return the optimal bess schedule."""
        lp = self.system_lp.lp
        efin_values = lp.get_col_sol(self.efin_cols.values())
        inflow_values = lp.get_col_sol(self.inflow_cols.values())
        outflow_values = lp.get_col_sol(self.outflow_cols.values())
        return BESSSched(
            uid=self.bess.uid,
            name=self.bess.name,
            block_efin_values=efin_values,
            block_inflow_values=inflow_values,
            block_outflow_values=outflow_values,
        )
