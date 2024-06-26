"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List
from dataclasses_json import DataClassJsonMixin

from gilda_opts.demand_sched import DemandSched
from gilda_opts.grid_sched import GridSched
from gilda_opts.tssa_sched import TSSASched
from gilda_opts.bess_sched import BESSSched
from gilda_opts.local_source_sched import LocalSourceSched


@dataclass
class SystemSched(DataClassJsonMixin):
    """
    System class.

    Attributes:
    -----------
    buses: List of electric buses included in the system problem.
    demands: List of electric demands
    grids: List of electric grid connections
    """

    name: str = ''
    uid: int = -1
    total_cost: float = 0
    solver_time: float = 0
    grids: List[GridSched] = field(default_factory=lambda: [])
    demands: List[DemandSched] = field(default_factory=lambda: [])
    tssas: List[TSSASched] = field(default_factory=lambda: [])
    besss: List[BESSSched] = field(default_factory=lambda: [])
    local_sources: List[LocalSourceSched] = field(default_factory=lambda: [])
