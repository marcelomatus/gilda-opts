"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.bess import BESS
from gilda_opts.block import Block
from gilda_opts.bus import Bus
from gilda_opts.cesa import CESA
from gilda_opts.demand import Demand
from gilda_opts.electric_car import ElectricCar
from gilda_opts.grid import Grid
from gilda_opts.line import Line
from gilda_opts.local_source import LocalSource
from gilda_opts.srts import SRTS
from gilda_opts.thermal_unit import ThermalUnit
from gilda_opts.tssa import TSSA


@dataclass(frozen=False)
class System(BaseClassJson):
    """
    System class.

    Attributes:
     name: System name
     uid: System uid
     intvar_type:  Integer variable type= 1:integers, 0: reals
     blocks: Block List
     block_durations: Duration list [h]
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

    intvar_type: int = 1

    blocks: List[Block] = field(default_factory=list)
    block_durations: List[float] = field(default_factory=list)

    buses: List[Bus] = field(default_factory=list)
    lines: List[Line] = field(default_factory=list)
    grids: List[Grid] = field(default_factory=list)
    demands: List[Demand] = field(default_factory=list)
    tssas: List[TSSA] = field(default_factory=list)
    cesas: List[CESA] = field(default_factory=list)
    besss: List[BESS] = field(default_factory=list)
    srtss: List[SRTS] = field(default_factory=list)
    thermal_units: List[ThermalUnit] = field(default_factory=list)
    local_sources: List[LocalSource] = field(default_factory=list)
    electric_cars: List[ElectricCar] = field(default_factory=list)

    #
    # Public methods
    #
    def get_intvar_type(self, block: Block):
        """Return the intvar_type for a block."""
        return self.intvar_type * block.intvar_type
