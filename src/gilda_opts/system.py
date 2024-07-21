"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List
from gilda_opts.baseclass_json import BaseClassJson

from gilda_opts.block import Block
from gilda_opts.bus import Bus
from gilda_opts.line import Line
from gilda_opts.demand import Demand
from gilda_opts.grid import Grid
from gilda_opts.tssa import TSSA
from gilda_opts.cesa import CESA
from gilda_opts.bess import BESS
from gilda_opts.srts import SRTS
from gilda_opts.thermal_unit import ThermalUnit
from gilda_opts.local_source import LocalSource
from gilda_opts.electric_car import ElectricCar


@dataclass(frozen=True)
class System(BaseClassJson):
    """
    System class.

    Attributes:
    -----------
    name: System name
    uid: System uid
    blocks: Block List
    buses: Bus List
    lines: Line List
    grids: Grid List
    demands: Demand List
    tssas: TSSA List
    cesas: CESA List
    besss: BESS List
    srtss: SRTS List
    thermal_units: ThermalUnit List
    local_sources: LocalSource List
    electric_cars: ElectricCar List
    """

    name: str = ""
    uid: int = -1
    blocks: List[Block] = field(default_factory=list)
    buses: List[Bus] = field(default_factory=lambda: [])
    lines: List[Line] = field(default_factory=lambda: [])
    grids: List[Grid] = field(default_factory=lambda: [])
    demands: List[Demand] = field(default_factory=lambda: [])
    tssas: List[TSSA] = field(default_factory=lambda: [])
    cesas: List[CESA] = field(default_factory=lambda: [])
    besss: List[BESS] = field(default_factory=lambda: [])
    srtss: List[SRTS] = field(default_factory=lambda: [])
    thermal_units: List[ThermalUnit] = field(default_factory=lambda: [])
    local_sources: List[LocalSource] = field(default_factory=lambda: [])
    electric_cars: List[ElectricCar] = field(default_factory=lambda: [])
