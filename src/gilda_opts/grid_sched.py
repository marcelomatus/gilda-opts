"""GridSched module contains the basic grid schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class GridSched(BaseClassJson):
    """
    A GridSched represents the grid schedule resulting from the optimization.

    Attributes:
     uid:              Grid unique id
     name:             Grid provider name
     injection_values: Grid optimal injection values
     withdrawn_values: Grid optimal withdrawn values
    """

    uid: int = -1
    name: str = ""
    injection_values: List[float] = field(default_factory=list)
    withdrawn_values: List[float] = field(default_factory=list)
