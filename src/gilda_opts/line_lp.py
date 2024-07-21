"""Contains the demnand_lp class."""

from gilda_opts.block import Block
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.line import Line
from gilda_opts.line_sched import LineSched
from gilda_opts.utils import get_value_at


class LineLP:
    """Represents a Line in the LP formulation."""

    def __init__(self, line: Line, system_lp=None):
        """Create the LineLP instance."""
        self.flow_ab_cols: dict[int, int] = {}
        self.flow_ba_cols: dict[int, int] = {}

        self.line = line
        self.system_lp = system_lp

    def add_block(
        self,
        bid: int,
        block: Block,  # pylint: disable=unused-argument
    ):
        """Add Line equations to a block."""
        lp: LinearProblem = self.system_lp.lp
        bus_a_lp = self.system_lp.get_bus_lp(self.line.bus_a_uid)
        bus_b_lp = self.system_lp.get_bus_lp(self.line.bus_b_uid)

        #
        # adding the flow variables
        #
        capacity = self.line.capacity
        losses = self.line.losses
        lossless = losses == 0
        max_flow = capacity * get_value_at(self.line.max_flow_profile_sched, bid, 1)
        min_flow = capacity * get_value_at(self.line.min_flow_profile_sched, bid, -1)

        flow_ab_col = lp.add_col(lb=min_flow if lossless else 0, ub=max_flow)
        bus_a_lp.add_block_load_col(bid, flow_ab_col, coeff=1)
        bus_b_lp.add_block_load_col(bid, flow_ab_col, coeff=-(1 - losses))
        self.flow_ab_cols[bid] = flow_ab_col

        if not lossless:
            flow_ba_col = lp.add_col(lb=0, ub=-min_flow)
            bus_b_lp.add_block_load_col(bid, flow_ba_col, coeff=1)
            bus_a_lp.add_block_load_col(bid, flow_ba_col, coeff=-(1 - losses))
            self.flow_ba_cols[bid] = flow_ba_col

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal line schedule."""
        lp = self.system_lp.lp
        flow_values = lp.get_col_sol(self.flow_ab_cols.values())
        if len(self.flow_ba_cols) > 0:
            flow_values -= lp.get_col_sol(self.flow_ba_cols.values())

        return LineSched(
            uid=self.line.uid,
            name=self.line.name,
            flow_values=flow_values,
        )
