"""LocalSourceSched module contains the basic local_source schedule."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class LocalSourceSched(DataClassJsonMixin):
    """
    A LocalSourceSched represents the local_source schedule resulting optimization.

    Attributes:
    ----------
    uid:              LocalSource unique id
    name:             LocalSource provider name
    injection_values: LocalSource optimal injection values
    """

    uid: int = -1
    name: str = ''
    block_injection_values: List[float] = field(default_factory=list)
