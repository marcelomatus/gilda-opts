"""TSSA module represents a Time Shift-able Smart Appliance load."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class TSSA(BaseClassJson):
    """TSSA represents the Time Shift-able Smart Appliance load in the scheduling problem."""

    #: TSSA unique id
    uid: int = -1

    #: TSSA name
    name: str = ""

    #: Bus uid to be connected to
    bus_uid: int = -1

    #: Load value [KW]
    load: float = 0

    #: 'On' continuous period time [H]
    on_period: float = 0

    #: List of block index where the onoff variable value is set to off
    off_indexes: List[int] = field(default_factory=list)
