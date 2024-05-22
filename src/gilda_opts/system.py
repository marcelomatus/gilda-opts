"""System class represents the scheduling object."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin

from gilda_opts.bus import Bus
from gilda_opts.demand import Demand


@dataclass
class SystemOptions():
    """SystemOptions class."""

    cfail: float = 1000
    integer_mode: int = 0


@dataclass
class System(DataClassJsonMixin):
    """System class."""

    name: str = ''
    uid: int = -1
    options: SystemOptions = field(default_factory=SystemOptions)
    buses: List[Bus] = field(default_factory=lambda: [])
    demands: List[Demand] = field(default_factory=lambda: [])
