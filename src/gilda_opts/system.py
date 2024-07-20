"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List
from gilda_opts.baseclass_json import BaseClassJson

from gilda_opts.block import Block
from gilda_opts.bus import Bus
from gilda_opts.demand import Demand
from gilda_opts.grid import Grid
from gilda_opts.tssa import TSSA
from gilda_opts.cesa import CESA
from gilda_opts.bess import BESS
from gilda_opts.sbtm import SBTM
from gilda_opts.local_source import LocalSource
from gilda_opts.electric_car import ElectricCar


@dataclass(frozen=True)
class System(BaseClassJson):
    """
    System class.

    Attributes:
    -----------
    blocks: List of blocks.
    buses: List of electric buses included in the system problem.
    demands: List of electric demands
    grids: List of electric grid connections
    """

    name: str = ""
    uid: int = -1
    blocks: List[Block] = field(default_factory=list)
    buses: List[Bus] = field(default_factory=lambda: [])
    grids: List[Grid] = field(default_factory=lambda: [])
    demands: List[Demand] = field(default_factory=lambda: [])
    tssas: List[TSSA] = field(default_factory=lambda: [])
    cesas: List[CESA] = field(default_factory=lambda: [])
    besss: List[BESS] = field(default_factory=lambda: [])
    sbtms: List[SBTM] = field(default_factory=lambda: [])
    local_sources: List[LocalSource] = field(default_factory=lambda: [])
    electric_cars: List[ElectricCar] = field(default_factory=lambda: [])
