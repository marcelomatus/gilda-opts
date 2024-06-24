"""GridSched module contains the basic grid schedule."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class GridSched(DataClassJsonMixin):
    """
    A GridSched represents the grid schedule resulting from the optimization.

    Attributes:
    ----------
    uid:              Grid unique id
    name:             Grid provider name
    injection_values: Grid optimal injection values
    purchase_values:  Grid optimal purchase values
    """

    uid: int = -1
    name: str = ''
    block_injection_values: List[float] = field(default_factory=list)
    block_purchase_values: List[float] = field(default_factory=list)
