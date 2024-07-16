"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem, guid
from gilda_opts.tssa import TSSA
from gilda_opts.tssa_sched import TSSASched


class TSSALP:
    """Represents a Block in the LP formulation."""

    def __init__(self, tssa: TSSA, system_lp=None):
        """Create the TSSALP instance."""
        self.onoff_cols = {}
        self.onoff_rows = {}
        self.noon_rows = {}
        self.period_row = None

        self.tssa = tssa
        self.system_lp = system_lp

    def add_block(
        self,
        index: int,
        block: Block,  # pylint: disable=unused-argument
    ):
        """Add TSSA equations to a block."""
        bid = index
        uid = self.tssa.uid
        lp: LinearProblem = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.tssa.bus_uid)

        #
        # adding the load variable
        #
        lname = guid("tu", uid, bid)
        load = self.tssa.load
        onoff_col = lp.add_col(name=lname, lb=0, ub=1, ctype=1)
        logging.info("added onoff variable %s %d", lname, onoff_col)

        self.onoff_cols[bid] = onoff_col
        bus_lp.add_block_load_col(bid, onoff_col, coeff=load)

        #
        # Setting the off value is needed
        #
        if index in self.tssa.off_indexes:
            lp.set_col_ub(onoff_col, cub=0)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        #
        # Adding onoff constraints
        #
        uid = self.tssa.uid
        lp = self.system_lp.lp
        inf = lp.inf

        #
        # Adding the period constraint
        #
        n = len(self.onoff_cols)
        d = [self.system_lp.system.blocks[i].duration for i in range(0, n)]

        row = {}
        for i in range(0, n):
            row[self.onoff_cols[i]] = d[i]
        lb = self.tssa.on_period
        lname = guid("tp", uid)
        period_row = lp.add_row(row, name=lname, lb=lb)
        logging.info("added period row %s %s %s", lname, period_row, lb)
        self.period_row = period_row

        #
        # Adding the continuous operation constraints
        #
        t_last = 0.0
        for i in range(n - 1, -1, -1):
            t_last += d[i]
            if t_last >= self.tssa.on_period:
                break

        n_last = i
        logging.info("n and n_last %d %d", n, n_last)

        for i in range(0, n_last):
            t_last = 0.0
            for ii in range(i + 1, n):
                t_last += d[ii]
                if t_last >= self.tssa.on_period:
                    break

            for z in range(i + 1, ii):
                row = {}
                uz = self.onoff_cols[z]
                ui = self.onoff_cols[i]
                if i == 0:
                    row[uz] = 1
                    row[ui] = -1
                    lb = -inf
                    ub = 0
                else:
                    uim1 = self.onoff_cols[i - 1]
                    row[uz] = 1
                    row[ui] = -1
                    row[uim1] = 1
                    lb = 0
                    ub = inf
                lname = guid("tu", uid, i, z)
                u_row = lp.add_row(row, name=lname, lb=lb, ub=ub)
                self.onoff_rows[(i, z)] = u_row
                logging.info("added urow %s %d %d %s", lname, i, z, row)

        #
        # Adding the no-on constraint in the border
        #
        for i in range(max(n_last, 1), n):
            row = {}
            uim1 = self.onoff_cols[i - 1]
            ui = self.onoff_cols[i]
            row[ui] = 1
            row[uim1] = -1
            lb = -inf
            ub = 0
            u_row = lp.add_row(row, name=lname, lb=lb, ub=ub)
            self.noon_rows[i] = u_row
            lname = guid("to", uid, i)
            logging.info("added no-on %s %s %s", lname, i, row)

    def get_sched(self):
        """Return the optimal tssa schedule."""
        lp = self.system_lp.lp
        onoff_values = lp.get_col_sol(self.onoff_cols.values())
        return TSSASched(
            uid=self.tssa.uid,
            name=self.tssa.name,
            block_onoff_values=onoff_values,
        )
