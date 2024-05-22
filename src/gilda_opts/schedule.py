"""Schedule class represents the scheduling object."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin

from gilda_opts.bus import Bus
from gilda_opts.demand import Demand


@dataclass
class ScheduleOptions():
    """ScheduleOptions class."""

    cfail: float = 1000
    integer_mode: int = 0


@dataclass
class Schedule(DataClassJsonMixin):
    """Schedule class."""

    name: str = ''
    uid: int = -1
    options: ScheduleOptions = field(default_factory=ScheduleOptions)
    buses: List[Bus] = field(default_factory=lambda: [])
    demands: List[Demand] = field(default_factory=lambda: [])
