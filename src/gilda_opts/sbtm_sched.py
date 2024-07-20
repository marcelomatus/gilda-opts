"""SBTMSched module contains the SBTM schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class SBTMSched(BaseClassJson):
    """
    A SBTMSched represents the sbtm schedule resulting from the optimization.

    Attributes:
    ----------
    uid:                 SBTM unique id
    name:                SBTM name
    tfin_values:         tfin_values
    onoff_heat_values:      onoff_heat_values
    onoff_cool_values:     onoff_cool_values
    """

    uid: int = -1
    name: str = ""
    tfin_values: List[float] = field(default_factory=list)
    onoff_heat_values: List[float] = field(default_factory=list)
    onoff_cool_values: List[float] = field(default_factory=list)
