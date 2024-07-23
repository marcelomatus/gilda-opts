"""System class represents the system object."""

from dataclasses import dataclass, field
from typing import List
from gilda_opts.baseclass_json import BaseClassJson

from gilda_opts.bus_sched import BusSched
from gilda_opts.line_sched import LineSched
from gilda_opts.demand_sched import DemandSched
from gilda_opts.grid_sched import GridSched
from gilda_opts.tssa_sched import TSSASched
from gilda_opts.cesa_sched import CESASched
from gilda_opts.bess_sched import BESSSched
from gilda_opts.srts_sched import SRTSSched
from gilda_opts.thermal_unit_sched import ThermalUnitSched
from gilda_opts.local_source_sched import LocalSourceSched
from gilda_opts.electric_car_sched import ElectricCarSched


@dataclass
class SystemSched(BaseClassJson):
    """
    SystemSched class, contains the system optimal scheduling.

    Attributes:
     name: System name
     uid: System uid
     total_cost: Total objective cost
     solver_time: Solver time
     buses: BusSched list
     lines: LineSched list
     grids: GridSched list
     demands: DemandSched list
     tssas: TSSASched list
     cesas: CESASched list
     besss: BESSSched list
     srtss: SRTSSched list
     thermal_units: ThermalUnitSched list
     local_sources: LocalSourceSched list
     electric_cars: ElectricCarSched list
    """

    name: str = ""
    uid: int = -1

    total_cost: float = 0
    solver_time: float = 0

    buses: List[BusSched] = field(default_factory=list)
    lines: List[LineSched] = field(default_factory=list)
    grids: List[GridSched] = field(default_factory=list)
    demands: List[DemandSched] = field(default_factory=list)
    tssas: List[TSSASched] = field(default_factory=list)
    cesas: List[CESASched] = field(default_factory=list)
    besss: List[BESSSched] = field(default_factory=list)
    srtss: List[SRTSSched] = field(default_factory=list)
    thermal_units: List[ThermalUnitSched] = field(default_factory=list)
    local_sources: List[LocalSourceSched] = field(default_factory=list)
    electric_cars: List[ElectricCarSched] = field(default_factory=list)
