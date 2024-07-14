"""CESA module represents a Cumulative Energy Smart Appliance load."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class CESA(BaseClassJson):
    """CESA represents the Cumulative Energy Smart Appliance load.

    This appliance requires to consume a given amount energy in specific block
    segment or energy blocks.

    For example, it may requires to consume 3 KWh every day.

    Attributes:
    -----------
    uid:          CESA unique id
    name:         CESA name
    bus_id:      Bus uid to be connected to
    load:         Load value [KW]
    cumulative_energies: Cumulative energy for each cumulative energy requirement [KWh]
    cumulative_indexes:  Index array that defines each block requirement assignment.

    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1
    load: float = 0
    cumulative_energies: List[float] = field(default_factory=list)
    cumulative_indexes: List[int] = field(default_factory=list)
