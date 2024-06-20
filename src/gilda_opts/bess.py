"""BESS module represents a Time Shift-able Smart Appliance load."""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class BESS(DataClassJsonMixin):
    """
    BESS represents the Time Shift-able Smart Appliance load in the scheduling problem.

    Attributes:
    -----------
    uid:          BESS unique id
    name:         BESS name
    bus_id:       Bus uid to be connected to
    capacity:     Storage capacity [KWh]
    max_flow:     Max In & Out flow [KW]
    efficiency:   In&Out efficiency [0..1]
    eini:         Start energy stored [KWh]
    efin:         End energy stored [KWh]
    efin_value:   Energy value at the end of the period [$/KWh]
    """

    uid: int = -1
    name: str = ''
    bus_uid: int = -1
    capacity: float = 0
    max_flow: float = 0
    efficiency: float = 1
    eini: float = 0
    efin: float = 0
    efin_value: float = 0
