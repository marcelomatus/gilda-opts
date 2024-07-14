"""Contains the demnand_lp class."""

import logging
from collections import defaultdict

from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem, guid
from gilda_opts.cesa import CESA
from gilda_opts.cesa_sched import CESASched


class CESALP:
    """Represents a Block in the LP formulation."""

    def __init__(self, cesa: CESA, system_lp=None):
        """Create the CESALP instance."""
        self.block_onoff_cols = {}

        self.cesa = cesa
        self.system_lp = system_lp

        self.energy_rows = {}
        self.cumulative_cols = defaultdict(list)

    def add_block(self, index: int, block: Block):
        """Add CESA equations to a block."""
        bid = index
        uid = self.cesa.uid
        lp: LinearProblem = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.cesa.bus_uid)

        #
        # adding the load variable
        #
        ce_group = -1
        try:
            ce_group = self.cesa.cumulative_indexes[bid]
        except IndexError:
            pass

        print("cesa %s", ce_group)
        if ce_group < 0:
            return

        lname = guid("ceu", uid, bid)
        load = self.cesa.load
        onoff_col = lp.add_col(name=lname, lb=0, ub=1, ctype=1)
        logging.info("added onoff variable %s %d", lname, onoff_col)

        self.block_onoff_cols[bid] = onoff_col
        bus_lp.add_block_load_col(bid, onoff_col, coeff=load)

        self.cumulative_cols[ce_group].append((block.duration, onoff_col))
        print("cc %s", self.cumulative_cols)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        #
        # Adding onoff constraints
        #
        uid = self.cesa.uid
        lp = self.system_lp.lp

        #
        # Adding the ce group constraint
        #
        print("pb %s", self.cumulative_cols)
        for group, cols in self.cumulative_cols.items():
            row = {}
            for duration, col in cols:
                row[col] = duration * self.cesa.load

            lb = self.cesa.cumulative_energies[group]
            lname = guid("ceg", uid)
            energy_row = lp.add_row(row, name=lname, lb=lb)
            logging.info("added period row %s %s %s", lname, energy_row, lb)
            self.energy_rows[group] = energy_row

    def get_sched(self):
        """Return the optimal cesa schedule."""
        lp = self.system_lp.lp
        block_onoff_values = lp.get_col_sol(self.block_onoff_cols.values())
        return CESASched(
            uid=self.cesa.uid,
            name=self.cesa.name,
            block_onoff_values=block_onoff_values,
        )
