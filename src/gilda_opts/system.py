"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin

from gilda_opts.bus import Bus
from gilda_opts.demand import Demand
from gilda_opts.grid import Grid


@dataclass
class System(DataClassJsonMixin):
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
    buses: List[Bus] = field(default_factory=lambda: [])
    demands: List[Demand] = field(default_factory=lambda: [])
    grids: List[Grid] = field(default_factory=lambda: [])
