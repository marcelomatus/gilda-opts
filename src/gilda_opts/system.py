"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin

from gilda_opts.block import Block
from gilda_opts.bus import Bus
from gilda_opts.demand import Demand
from gilda_opts.grid import Grid
from gilda_opts.tssa import TSSA


@dataclass
class System(DataClassJsonMixin):
    """
    System class.

    Attributes:
    -----------
    blocks: List of blocks.
    buses: List of electric buses included in the system problem.
    demands: List of electric demands
    grids: List of electric grid connections
    """

    name: str = ''
    uid: int = -1
    blocks: List[Block] = field(default_factory=list)
    buses: List[Bus] = field(default_factory=lambda: [])
    grids: List[Grid] = field(default_factory=lambda: [])
    demands: List[Demand] = field(default_factory=lambda: [])
    tssas: List[TSSA] = field(default_factory=lambda: [])
