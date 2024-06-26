"""Demand module represents a base electric load."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class Demand(DataClassJsonMixin):
    """
    Demand represents the base electric load in the scheduling problem.

    Attributes:
    -----------
    uid:     Load unique id
    name:    Load name
    bus_uid: Bus uid to be connected to
    loads:   List of load values [KW]
    """

    uid: int = -1
    name: str = ''
    bus_uid: int = -1
    loads: List[float] = field(default_factory=list)
    cfail: float = 0
