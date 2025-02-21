"""Contains the demnand_lp class."""

from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.tssa import TSSA
from gilda_opts.tssa_sched import TSSASched


class TSSALP:
    """Represents a Block in the LP formulation."""

    def __init__(self, tssa: TSSA, system_lp=None):
        """Create the TSSALP instance."""
        self.onoff_cols: dict[int, int] = {}
        self.onoff_rows: dict[tuple[int, int], int] = {}
        self.noon_rows: dict[int, int] = {}
        self.period_row = None

        self.tssa = tssa
        self.system_lp = system_lp

    def add_block(
        self,
        bid: int,
        block: Block,  # pylint: disable=unused-argument
    ):
        """Add TSSA equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.tssa.bus_uid)
        intvar_type = self.system_lp.system.get_intvar_type(block)

        #
        # adding the load variable
        #
        load = self.tssa.load
        onoff_col = lp.add_col(lb=0, ub=1, ctype=intvar_type)

        self.onoff_cols[bid] = onoff_col
        bus_lp.add_block_load_col(bid, onoff_col, coeff=load)

        #
        # Setting the off value is needed
        #
        if bid in self.tssa.off_indexes:
            lp.set_col_ub(onoff_col, cub=0)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""
        #
        # Adding onoff constraints
        #
        lp = self.system_lp.lp
        inf = lp.inf

        #
        # Adding the period constraint
        #
        n = len(self.onoff_cols)
        if n == 0:
            return
        
        d = [self.system_lp.system.blocks[i].duration for i in range(0, n)]

        row = {}
        for i in range(0, n):
            row[self.onoff_cols[i]] = d[i]
        lb = self.tssa.on_period
        period_row = lp.add_row(row, lb=lb)
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

                u_row = lp.add_row(row, lb=lb, ub=ub)
                self.onoff_rows[(i, z)] = u_row

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
            u_row = lp.add_row(row, lb=lb, ub=ub)
            self.noon_rows[i] = u_row

    def get_sched(self):
        """Return the optimal tssa schedule."""
        lp = self.system_lp.lp
        onoff_values = lp.get_col_sol(self.onoff_cols.values())
        return TSSASched(
            uid=self.tssa.uid,
            name=self.tssa.name,
            onoff_values=onoff_values,
        )
