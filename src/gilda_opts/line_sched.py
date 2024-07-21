"""LineSched module contains the Line schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class LineSched(BaseClassJson):
    """
    A LineSched represents the line schedule resulting from the optimization.

    Attributes:
    ----------
    uid:          Line unique id
    name:         Line provider name
    flow_values: Line optimal flow ab values
    """

    uid: int = -1
    name: str = ""
    flow_values: List[float] = field(default_factory=list)
