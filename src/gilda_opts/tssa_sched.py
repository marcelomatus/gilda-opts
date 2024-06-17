"""TSSASched module contains the TSSA schedule."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class TSSASched(DataClassJsonMixin):
    """
    A TSSASched represents the tssa schedule resulting from the optimization.

    Attributes:
    ----------
    uid:          TSSA unique id
    name:         TSSA provider name
    onoff_values: TSSA optimal onoff values
    """

    uid: int = -1
    name: str = ''
    block_onoff_values: List[float] = field(default_factory=list)
