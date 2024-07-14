"""BESSSched module contains the BESS schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class BESSSched(BaseClassJson):
    """
    A BESSSched represents the bess schedule resulting from the optimization.

    Attributes:
    ----------
    uid:          BESS unique id
    name:         BESS provider name
    onoff_values: BESS optimal onoff values
    """

    uid: int = -1
    name: str = ""
    block_efin_values: List[float] = field(default_factory=list)
    block_inflow_values: List[float] = field(default_factory=list)
    block_outflow_values: List[float] = field(default_factory=list)
