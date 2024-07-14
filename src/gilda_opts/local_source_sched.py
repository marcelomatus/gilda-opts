"""LocalSourceSched module contains the basic local_source schedule."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class LocalSourceSched(BaseClassJson):
    """A LocalSourceSched represents the local_source schedule resulting optimization.

    Attributes:
    ----------
    uid:              LocalSource unique id
    name:             LocalSource provider name
    generation_values: LocalSource optimal generation values
    """

    uid: int = -1
    name: str = ""
    block_generation_values: List[float] = field(default_factory=list)
