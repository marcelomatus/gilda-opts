"""Contains the demnand_lp class."""

from gilda_opts.bess import Battery, BESS
from gilda_opts.bess_sched import BESSSched
from gilda_opts.block import Block
from gilda_opts.bus_lp import BusLP
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.utils import get_value_at


class BESSLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, bess: BESS, system_lp=None):
        """Create the BESSLP instance."""
        self.flow_in_cols: dict[int, int] = {}
        self.flow_out_cols: dict[int, int] = {}
        self.efin_cols: dict[int, int] = {}
        self.efin_rows: dict[int, int] = {}

        self.bess = bess
        self.system_lp = system_lp

    @staticmethod
    def add_block_i(
        lp: LinearProblem,
        bid: int,
        block: Block,
        prev_efin_col: int,
        bess: Battery,
        bus_lp: BusLP | None = None,
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
        #
        # flow_in col
        #
        ub = bess.max_flow_in if bus_lp is not None else 0
        flow_in_col = lp.add_col(lb=0, ub=ub)

        #
        # flow_out col
        #
        cvar = block.energy_cost(bess.discharge_cost)
        ub = bess.max_flow_out if bus_lp is not None else 0
        flow_out_col = lp.add_col(lb=0, ub=ub, c=cvar)

        #
        # adding the flows to the bus
        #
        if bus_lp is not None:
            bus_lp.add_block_load_col(bid, flow_in_col, coeff=+1.0)
            bus_lp.add_block_load_col(bid, flow_out_col, coeff=-1.0)

        #
        # efin col
        #
        lb = bess.capacity * get_value_at(bess.emin_profile_sched, bid, 0)
        ub = bess.capacity * get_value_at(bess.emax_profile_sched, bid, 1)
        efin_col = lp.add_col(lb=lb, ub=ub)

        #
        # efin row
        #
        row: dict[int, float] = {}
        row[efin_col] = 1
        row[flow_in_col] = -block.duration * bess.efficiency_in
        row[flow_out_col] = block.duration / bess.efficiency_out

        if prev_efin_col < 0:
            lb, ub = bess.eini, bess.eini
        else:
            lb, ub = 0, 0
            row[prev_efin_col] = -1

        efin_row = lp.add_row(row, lb=lb, ub=ub)

        return flow_in_col, flow_out_col, efin_col, efin_row

    def add_block(self, bid: int, block: Block):
        """Add BESS equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.bess.bus_uid)
        prev_efin_col = self.efin_cols[bid - 1] if bid > 0 else -1

        flow_in_col, flow_out_col, efin_col, efin_row = BESSLP.add_block_i(
            lp=lp,
            bid=bid,
            block=block,
            prev_efin_col=prev_efin_col,
            bess=self.bess,
            bus_lp=bus_lp,
        )

        self.flow_out_cols[bid] = flow_out_col
        self.flow_in_cols[bid] = flow_in_col
        self.efin_cols[bid] = efin_col
        self.efin_rows[bid] = efin_row

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
        flow_in_values = lp.get_col_sol(self.flow_in_cols.values())
        flow_out_values = lp.get_col_sol(self.flow_out_cols.values())
        return BESSSched(
            uid=self.bess.uid,
            name=self.bess.name,
            efin_values=efin_values,
            flow_in_values=flow_in_values,
            flow_out_values=flow_out_values,
        )
