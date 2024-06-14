"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin

from gilda_opts.demand_sched import DemandSched
from gilda_opts.grid_sched import GridSched


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
    demands: List[DemandSched] = field(default_factory=lambda: [])
    grids: List[GridSched] = field(default_factory=lambda: [])
