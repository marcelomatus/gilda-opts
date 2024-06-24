"""Contains the demnand_lp class."""

import logging

from gilda_opts.block import Block
from gilda_opts.local_source import LocalSource
from gilda_opts.local_source_sched import LocalSourceSched
from gilda_opts.linear_problem import guid


class LocalSourceLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, local_source: LocalSource, system_lp=None):
        """Create the LocalSourceLP instance."""
        self.block_injection_cols = {}
        self.block_pmax_rows = {}
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
        # adding the local_source injection variable
        #

        lname = guid('lb', uid, bid)
        try:
            gprof = self.local_source.gen_profile[bid]
        except IndexError:
            gprof = 0

        pmax = self.local_source.capacity*gprof

        injection_col = lp.add_col(name=lname, lb=0, ub=pmax)
        logging.info('added injection variable %s %s', lname, injection_col)

        self.block_injection_cols[bid] = injection_col
        bus_lp.add_block_load_col(bid, injection_col, coeff=-1)

    def post_blocks(self):
        """Close the LP formulation post the blocks formulation."""

    def get_sched(self):
        """Return the optimal local_source schedule."""
        lp = self.system_lp.lp
        block_injection_values = lp.get_col_sol(self.block_injection_cols.values())
        return LocalSourceSched(uid=self.local_source.uid,
                                name=self.local_source.name,
                                block_injection_values=block_injection_values)
