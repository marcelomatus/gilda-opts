"""Contains the demnand_lp class."""

from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.cesa import CESA
from gilda_opts.cesa_sched import CESASched
from gilda_opts.utils import get_value_at


class CESALP:
    """Represents a Block in the LP formulation."""

    def __init__(self, cesa: CESA, system_lp=None):
        """Create the CESALP instance."""
        self.onoff_cols: dict[int, int] = {}
        self.on_period_rows: dict[int, int] = {}
        self.energy_rows: dict[int, int] = {}
        self.onoff_ctypes: dict[int, int] = {}
        self.cumulative_cols: list = []

        self.cesa = cesa
        self.system_lp = system_lp

    def add_block(self, bid: int, block: Block):
        """Add CESA equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.cesa.bus_uid)

        intvar_type = self.system_lp.system.get_intvar_type(block)
        #
        # adding the load variable
        #
        cmask = get_value_at(self.cesa.cumulative_mask_sched, bid, 0)

        if cmask <= 0:
            return

        onoff_col = lp.add_col(lb=0, ub=1)

        self.onoff_cols[bid] = onoff_col
        load = self.cesa.load
        bus_lp.add_block_load_col(bid, onoff_col, coeff=load)

        self.onoff_ctypes[onoff_col] = intvar_type
        self.cumulative_cols.append((cmask, block.duration, onoff_col))

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        lp: LinearProblem = self.system_lp.lp

        #
        # Adding the cumulative on_period constraints
        #
        for i, on_period in enumerate(self.cesa.cumulative_on_periods):
            emask = pow(2, i + 1)
            row = {}
            for cmask, duration, onoff_col in self.cumulative_cols:
                if emask ^ cmask != 0:
                    row[onoff_col] = duration
                    ctype = self.onoff_ctypes[onoff_col]
                    lp.set_col_ctype(onoff_col, ctype)

            on_period_row = lp.add_row(row, lb=on_period)
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

            energy_row = lp.add_row(row, lb=energy)
            self.energy_rows[i] = energy_row

    def get_sched(self):
        """Return the optimal cesa schedule."""
        lp = self.system_lp.lp
        onoff_values = lp.get_col_sol(self.onoff_cols.values())
        return CESASched(
            uid=self.cesa.uid,
            name=self.cesa.name,
            onoff_values=onoff_values,
        )
