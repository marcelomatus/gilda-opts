"""GridSched module contains the basic grid schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class DemandSched(BaseClassJson):
    """
    A DemandSched represents the demand schedule resulting from the optimization.

    Attributes:
     uid:              Demand unique id
     name:             Demand provider name
     load_values: Demand optimal load values
    """

    uid: int = -1
    name: str = ""
    load_values: List[float] = field(default_factory=list)
    fail_values: List[float] = field(default_factory=list)
