"""ThermalUnitSched module contains the ThermalUnit schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class ThermalUnitSched(BaseClassJson):
    """
    A ThermalUnitSched represents the thermal_unit schedule.

    Attributes:
    ----------
    uid:            ThermalUnit unique id
    name:           ThermalUnit name
    onoff_values:   onoff_cool_values
    """

    uid: int = -1
    name: str = ""
    onoff_values: List[float] = field(default_factory=list)
