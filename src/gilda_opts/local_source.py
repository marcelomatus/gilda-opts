"""LocalSource module contains the basic local energy source, such as PV or Wind."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class LocalSource(DataClassJsonMixin):
    """
    A LocalSource represents a local energy source .

    Attributes:
    ----------
    uid:                LocalSource unique id
    name:               LocalSource provider name
    capacity:           Connection Capacity [KW]
    generation_profile: Potential generation profile value, as a factor of the
                        capacity [0..1]
    """

    uid: int = -1
    name: str = ''
    bus_uid: int = -1
    capacity: float = 0
    generation_profile: List[float] = field(default_factory=list)
