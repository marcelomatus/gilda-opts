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
    """System class."""

    #: System name
    name: str = ""
    #: System uid
    uid: int = -1

    #: Integer variable type= 1:integers, 0: reals
    intvar_type: int = 1

    #: Block List
    blocks: List[Block] = field(default_factory=list)
    #: Duration list [h]
    block_durations: List[float] = field(default_factory=list)

    #: Bus List
    buses: List[Bus] = field(default_factory=list)
    #: Line List
    lines: List[Line] = field(default_factory=list)
    #: Grid List
    grids: List[Grid] = field(default_factory=list)
    #: Demand List
    demands: List[Demand] = field(default_factory=list)
    #: TSSA List
    tssas: List[TSSA] = field(default_factory=list)
    #: CESA List
    cesas: List[CESA] = field(default_factory=list)
    #: BESS List
    besss: List[BESS] = field(default_factory=list)
    #: SRTS List
    srtss: List[SRTS] = field(default_factory=list)
    #: ThermalUnit List
    thermal_units: List[ThermalUnit] = field(default_factory=list)
    #: LocalSource List
    local_sources: List[LocalSource] = field(default_factory=list)
    #: ElectricCar List
    electric_cars: List[ElectricCar] = field(default_factory=list)

    #
    # Public methods
    #
    def get_intvar_type(self, block: Block):
        """Return the intvar_type for a block."""
        return self.intvar_type * block.intvar_type
