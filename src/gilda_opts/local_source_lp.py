"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.linear_problem import guid
from gilda_opts.local_source import LocalSource
from gilda_opts.local_source_sched import LocalSourceSched
from gilda_opts.utils import get_number_at


class LocalSourceLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, local_source: LocalSource, system_lp=None):
        """Create the LocalSourceLP instance."""
        self.generation_cols: dict[int, int] = {}
        self.pmax_rows: dict[int, int] = {}
        self.pmax_col = -1

        self.local_source = local_source
        self.system_lp = system_lp

    def add_block(self, index: int, block: Block):  # pylint: disable=W0613
        """Add LocalSource equations to a block."""
        bid = index
        uid = self.local_source.uid
        lp = self.system_lp.lp
        bus_lp = self.system_lp.get_bus_lp(self.local_source.bus_uid)

        #
        # adding the local_source generation variable
        #

        lname = guid("lb", uid, bid)
        gprof = get_number_at(self.local_source.generation_profile, bid, 1)

        pmax = self.local_source.capacity * gprof

        generation_col = lp.add_col(name=lname, lb=0, ub=pmax)
        logging.info("added generation variable %s %s", lname, generation_col)

        self.generation_cols[bid] = generation_col
        bus_lp.add_block_load_col(bid, generation_col, coeff=-1)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal local_source schedule."""
        lp = self.system_lp.lp
        generation_values = lp.get_col_sol(self.generation_cols.values())
        return LocalSourceSched(
            uid=self.local_source.uid,
            name=self.local_source.name,
            generation_values=generation_values,
        )
