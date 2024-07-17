"""TSSASched module contains the TSSA schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class TSSASched(BaseClassJson):
    """
    A TSSASched represents the tssa schedule resulting from the optimization.

    Attributes:
    ----------
    uid:          TSSA unique id
    name:         TSSA provider name
    onoff_values: TSSA optimal onoff values
    """

    uid: int = -1
    name: str = ""
    onoff_values: List[float] = field(default_factory=list)
