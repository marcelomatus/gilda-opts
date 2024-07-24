"""Contains the system_lp class."""

from typing import List

from gilda_opts.bess_lp import BESSLP
from gilda_opts.srts_lp import SRTSLP
from gilda_opts.thermal_unit_lp import ThermalUnitLP
from gilda_opts.block import Block
from gilda_opts.bus_lp import BusLP
from gilda_opts.line_lp import LineLP
from gilda_opts.demand_lp import DemandLP
from gilda_opts.grid_lp import GridLP
from gilda_opts.linear_problem import LinearProblem
from gilda_opts.system import System
from gilda_opts.system_sched import SystemSched
from gilda_opts.tssa_lp import TSSALP
from gilda_opts.cesa_lp import CESALP
from gilda_opts.local_source_lp import LocalSourceLP
from gilda_opts.electric_car_lp import ElectricCarLP


class SystemLP:
    """Represents a Block in the LP formulation."""

    def __init__(self, system: System, lp: LinearProblem | None = None):
        """Create the SystemLP instance."""
        self.load_rows: dict[int, int] = {}
        self.lp = lp if lp is not None else LinearProblem()

        if len(system.blocks) == 0:
            system.blocks = [Block(duration=d) for d in system.block_durations]

        self.system = system

        self.buses_lp = self.create_collection(system.buses, BusLP)
        self.lines_lp = self.create_collection(system.lines, LineLP)
        self.srtss_lp = self.create_collection(system.srtss, SRTSLP)
        self.demands_lp = self.create_collection(system.demands, DemandLP)
        self.tssas_lp = self.create_collection(system.tssas, TSSALP)
        self.cesas_lp = self.create_collection(system.cesas, CESALP)
        self.grids_lp = self.create_collection(system.grids, GridLP)
        self.besss_lp = self.create_collection(system.besss, BESSLP)
        self.thermal_units_lp = self.create_collection(
            system.thermal_units, ThermalUnitLP
        )
        self.local_sources_lp = self.create_collection(
            system.local_sources, LocalSourceLP
        )
        self.electric_cars_lp = self.create_collection(
            system.electric_cars, ElectricCarLP
        )

        self.add_blocks(self.system.blocks)

    def create_collection(self, elements, collection_class):
        """Create a collection of lp elements."""
        collection = {}
        for e in elements:
            collection[e.uid] = collection_class(e, self)

        return collection

    def add_blocks_to_collection(self, collection, blocks):
        """Add blocks to a collections."""
        for bid, block in enumerate(blocks):
            for olp in collection.values():
                olp.add_block(bid, block)

        for olp in collection.values():
            olp.post_blocks()

    def add_blocks(self, blocks: List[Block]):
        """Add System equations to a block."""
        self.add_blocks_to_collection(self.buses_lp, blocks)
        self.add_blocks_to_collection(self.lines_lp, blocks)
        self.add_blocks_to_collection(self.grids_lp, blocks)
        self.add_blocks_to_collection(self.demands_lp, blocks)
        self.add_blocks_to_collection(self.tssas_lp, blocks)
        self.add_blocks_to_collection(self.cesas_lp, blocks)
        self.add_blocks_to_collection(self.besss_lp, blocks)
        self.add_blocks_to_collection(self.srtss_lp, blocks)
        self.add_blocks_to_collection(self.thermal_units_lp, blocks)
        self.add_blocks_to_collection(self.local_sources_lp, blocks)
        self.add_blocks_to_collection(self.electric_cars_lp, blocks)

    def get_bus_lp(self, bus_uid: int) -> BusLP:
        """Return the bus_lp element for the bus_uid."""
        bus_lp: BusLP = self.buses_lp[bus_uid]
        return bus_lp

    def get_srts_lp(self, srts_uid: int) -> SRTSLP:
        """Return the srts_lp element for the srts_uid."""
        srts_lp: SRTSLP = self.srtss_lp[srts_uid]
        return srts_lp

    def solve(self, **kwargs):
        """Optimize the system for a list block definition."""
        self.lp.solve(**kwargs)
        return self.lp.get_status()

    def get_sched(self):
        """Return the system sched."""
        buses_sched = [o.get_sched() for o in self.buses_lp.values()]
        lines_sched = [o.get_sched() for o in self.lines_lp.values()]
        demands_sched = [o.get_sched() for o in self.demands_lp.values()]
        tssas_sched = [o.get_sched() for o in self.tssas_lp.values()]
        cesas_sched = [o.get_sched() for o in self.cesas_lp.values()]
        grids_sched = [o.get_sched() for o in self.grids_lp.values()]
        besss_sched = [o.get_sched() for o in self.besss_lp.values()]
        srtss_sched = [o.get_sched() for o in self.srtss_lp.values()]
        thermal_units_sched = [o.get_sched() for o in self.thermal_units_lp.values()]
        local_sources_sched = [o.get_sched() for o in self.local_sources_lp.values()]
        electric_cars_sched = [o.get_sched() for o in self.electric_cars_lp.values()]

        return SystemSched(
            name=self.system.name,
            uid=self.system.uid,
            total_cost=self.lp.get_obj(),
            solver_time=self.lp.get_time(),
            grids=grids_sched,
            buses=buses_sched,
            lines=lines_sched,
            demands=demands_sched,
            tssas=tssas_sched,
            cesas=cesas_sched,
            besss=besss_sched,
            srtss=srtss_sched,
            thermal_units=thermal_units_sched,
            local_sources=local_sources_sched,
            electric_cars=electric_cars_sched,
        )
