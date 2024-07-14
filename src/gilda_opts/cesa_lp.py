"""Contains the demnand_lp class."""

import logging

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

        self.on_period_rows = {}
        self.energy_rows = {}
        self.cumulative_cols = []

    def add_block(self, index: int, block: Block):
        """Add CESA equations to a block."""
        bid = index
        uid = self.cesa.uid
        lp: LinearProblem = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.cesa.bus_uid)

        #
        # adding the load variable
        #
        cmask = 0
        try:
            cmask = self.cesa.cumulative_masks[bid]
        except IndexError:
            pass

        if cmask <= 0:
            return

        lname = guid("ceu", uid, bid)
        col_type = 1 if len(self.cesa.cumulative_on_periods) != 0 else 0
        onoff_col = lp.add_col(name=lname, lb=0, ub=1, ctype=col_type)
        logging.info("added onoff variable %s %d", lname, onoff_col)

        self.block_onoff_cols[bid] = onoff_col
        load = self.cesa.load
        bus_lp.add_block_load_col(bid, onoff_col, coeff=load)

        self.cumulative_cols.append((cmask, block.duration, onoff_col))

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        #
        # Adding onoff constraints
        #
        uid = self.cesa.uid
        lp = self.system_lp.lp

        #
        # Adding the cumulative on_period constraints
        #
        for i, on_period in enumerate(self.cesa.cumulative_on_periods):
            emask = pow(2, i + 1)
            row = {}
            for cmask, duration, onoff_col in self.cumulative_cols:
                if emask ^ cmask != 0:
                    row[onoff_col] = duration

            lname = guid("ceg", uid, i)
            on_period_row = lp.add_row(row, name=lname, lb=on_period)
            logging.info("added period row %s %s %s", lname, on_period_row, on_period)
            self.on_period_rows[i] = on_period_row

        #
        # Adding the cumulative energy constraints
        #
        for i, energy in enumerate(self.cesa.cumulative_energies):
            emask = pow(2, i + 1)
            row = {}
            for cmask, duration, onoff_col in self.cumulative_cols:
                if emask ^ cmask != 0:
                    row[onoff_col] = duration * self.cesa.load

            lname = guid("ceg", uid, i)
            energy_row = lp.add_row(row, name=lname, lb=energy)
            logging.info("added period row %s %s %s", lname, energy_row, energy)
            self.energy_rows[i] = energy_row

    def get_sched(self):
        """Return the optimal cesa schedule."""
        lp = self.system_lp.lp
        block_onoff_values = lp.get_col_sol(self.block_onoff_cols.values())
        return CESASched(
            uid=self.cesa.uid,
            name=self.cesa.name,
            block_onoff_values=block_onoff_values,
        )
