"""BusSched module contains the Bus schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class BusSched(BaseClassJson):
    """
    A BusSched represents the bus schedule resulting from the optimization.

    Attributes:
     uid:             Bus unique id
     name:            Bus name
     efin_values:     efin_values
     flow_in_values:  flow_in_values
     flow_out_values: flow_out_values
    """

    uid: int = -1
    name: str = ""
    load_duals: List[float] = field(default_factory=list)
