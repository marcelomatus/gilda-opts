"""Contains the system_lp class."""
from typing import List

from gilda_opts.bess_lp import BESSLP
from gilda_opts.block import Block
from gilda_opts.bus_lp import BusLP
from gilda_opts.demand_lp import DemandLP
from gilda_opts.grid_lp import GridLP
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.system import System
from gilda_opts.system_sched import SystemSched
from gilda_opts.tssa_lp import TSSALP
from gilda_opts.local_source_lp import LocalSourceLP


class SystemLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, system: System, lp: LinearProblem = None):
        """Create the SystemLP instance."""
        self.block_load_rows = {}
        self.system = system
        self.lp = lp if lp is not None else LinearProblem()

        self.buses_lp = self.create_collection(system.buses, BusLP)
        self.demands_lp = self.create_collection(system.demands, DemandLP)
        self.tssas_lp = self.create_collection(system.tssas, TSSALP)
        self.grids_lp = self.create_collection(system.grids, GridLP)
        self.besss_lp = self.create_collection(system.besss, BESSLP)
        self.local_sources_lp = self.create_collection(system.local_sources,
                                                       LocalSourceLP)

        self.add_blocks(self.system.blocks)

    def create_collection(self, elements, collection_class):
        """Create a collection of lp elements."""
        collection = {}
        for e in elements:
            collection[e.uid] = collection_class(e, self)

        return collection

    def add_blocks_to_collection(self, collection, blocks):
        """Add blocks to a collections."""
        for index, block in enumerate(blocks):
            for olp in collection.values():
                olp.add_block(index, block)

        for olp in collection.values():
            olp.post_blocks()

    def add_blocks(self, blocks: List[Block]):
        """Add System equations to a block."""
        self.add_blocks_to_collection(self.buses_lp, blocks)
        self.add_blocks_to_collection(self.grids_lp, blocks)
        self.add_blocks_to_collection(self.demands_lp, blocks)
        self.add_blocks_to_collection(self.tssas_lp, blocks)
        self.add_blocks_to_collection(self.besss_lp, blocks)
        self.add_blocks_to_collection(self.local_sources_lp, blocks)

    def get_bus_lp(self, bus_uid):
        """Return the bus_lp element for the bus_uid."""
        return self.buses_lp[bus_uid]

    def solve(self, **kwargs):
        """Optimize the system for a list block definition."""
        self.lp.solve(**kwargs)
        return self.lp.get_status()

    def get_sched(self):
        """Return the system sched."""
        demands_sched = [o.get_sched() for o in self.demands_lp.values()]
        tssas_sched = [o.get_sched() for o in self.tssas_lp.values()]
        grids_sched = [o.get_sched() for o in self.grids_lp.values()]
        besss_sched = [o.get_sched() for o in self.besss_lp.values()]
        local_sources_sched = [o.get_sched() for o in self.local_sources_lp.values()]

        return SystemSched(name=self.system.name,
                           uid=self.system.uid,
                           total_cost=self.lp.get_obj(),
                           solver_time=self.lp.get_time(),
                           grids=grids_sched,
                           demands=demands_sched,
                           tssas=tssas_sched,
                           besss=besss_sched,
                           local_sources=local_sources_sched)
