"""SRTSSched module contains the SRTS schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class SRTSSched(BaseClassJson):
    """
    A SRTSSched represents the srts schedule resulting from the optimization.

    Attributes:
    ----------
    uid:                 SRTS unique id
    name:                SRTS name
    tfin_values:         tfin_values
    """

    uid: int = -1
    name: str = ""
    tfin_duals: List[float] = field(default_factory=list)
    tfin_values: List[float] = field(default_factory=list)
