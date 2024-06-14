"""GridSched module contains the basic grid schedule."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class DemandSched(DataClassJsonMixin):
    """
    A DemandSched represents the demand schedule resulting from the optimization.

    Attributes:
    ----------
    uid:              Demand unique id
    name:             Demand provider name
    load_values: Demand optimal load values
    """

    uid: int = -1
    name: str = ''
    block_load_values: List[float] = field(default_factory=list)
    block_fail_values: List[float] = field(default_factory=list)
