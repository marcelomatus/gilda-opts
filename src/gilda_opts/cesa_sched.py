"""CESASched module contains the CESA schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class CESASched(BaseClassJson):
    """
    A CESASched represents the cesa schedule resulting from the optimization.

    Attributes:
    ----------
    uid:          CESA unique id
    name:         CESA provider name
    onoff_values: CESA optimal onoff values
    """

    uid: int = -1
    name: str = ""
    block_onoff_values: List[float] = field(default_factory=list)
