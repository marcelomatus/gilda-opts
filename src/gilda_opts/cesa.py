"""CESA module represents a Cumulative Energy Smart Appliance load."""

from dataclasses import dataclass, field
from typing import List


from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import IntSched


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
    bus_uid:      Bus uid to be connected to
    load:         Load value [KW]
    cumulative_mask_sched:  Mask array for each block
    cumulative_on_periods: Cumulative on periods [h]
    cumulative_energies: Cumulative energies [KWh]


    CESA uses the mask concept to assign the on/off per block variables to the
    cumulative on_period or energy constraints.

    Usually you should provide one or the other. If the load only operates in a
    on/off state, use on_period. If you provide on_periods, the on&off
    variables will be binary.

    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1
    load: float = 0
    cumulative_mask_sched: IntSched = 0
    cumulative_on_periods: List[float] = field(default_factory=list)
    cumulative_energies: List[float] = field(default_factory=list)
