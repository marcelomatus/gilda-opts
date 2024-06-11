"""Contains the system_lp class."""
from typing import List

from gilda_opts.block import Block
from gilda_opts.bus_lp import BusLP
from gilda_opts.demand_lp import DemandLP
from gilda_opts.grid_lp import GridLP
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.system import System


class SystemLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, system: System, lp: LinearProblem):
        """Create the SystemLP instance."""
        self.block_load_rows = {}
        self.system = system
        self.lp = lp

        self.buses_lp = self.create_collection(system.buses, BusLP)
        self.demands_lp = self.create_collection(system.demands, DemandLP)
        self.grids_lp = self.create_collection(system.grids, GridLP)

    def create_collection(self, elements, collection_class):
        """Create a collection of lp elements."""
        collection = {}
        for e in elements:
            collection[e.uid] = collection_class(e, self)

        return collection

    def add_blocks_to_collection(self, collection, blocks):
        """Add blocks to a collections."""
        for block in blocks:
            for olp in collection.values():
                olp.add_block(block)

    def add_blocks(self, blocks: List[Block]):
        """Add System equations to a block."""
        self.add_blocks_to_collection(self.buses_lp, blocks)
        self.add_blocks_to_collection(self.demands_lp, blocks)
        self.add_blocks_to_collection(self.grids_lp, blocks)

    def get_bus_lp(self, bus_uid):
        """Return the bus_lp element for the bus_uid."""
        return self.buses_lp[bus_uid]
