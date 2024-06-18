"""TSSA module represents a Time Shift-able Smart Appliance load."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class TSSA(DataClassJsonMixin):
    """
    TSSA represents the Time Shift-able Smart Appliance load in the scheduling problem.

    Attributes:
    -----------
    uid:          TSSA unique id
    name:         TSSA name
    bus_id:       Bus uid to be connected to
    load:         Load value [KW]
    on_period:    'On' continuous period time [H]
    off_indexes:  List of block index where the onoff variable value is set to off
    """

    uid: int = -1
    name: str = ''
    bus_uid: int = -1
    load: float = 0
    on_period: float = 0
    off_indexes: List[int] = field(default_factory=list)
