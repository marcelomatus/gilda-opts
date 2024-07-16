"""ElectricCarSched module contains the ElectricCar schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class ElectricCarSched(BaseClassJson):
    """
    A ElectricCarSched represents the bess schedule resulting from the optimization.

    Attributes:
    ----------
    uid:                          ElectricCar unique id
    name:                         ElectricCar name
    battery_efin_values:    battery efin_values
    battery_flow_in_values:  battery flow_in_values
    battery_flow_out_values: battery flow_out_values
    engine_flow_values:     engine flow values
    """

    uid: int = -1
    name: str = ""
    block_battery_efin_values: List[float] = field(default_factory=list)
    block_battery_flow_in_values: List[float] = field(default_factory=list)
    block_battery_flow_out_values: List[float] = field(default_factory=list)
    block_engine_flow_values: List[float] = field(default_factory=list)
