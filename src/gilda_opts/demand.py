"""Demand module contains the base electric load."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class Demand(DataClassJsonMixin):
    """
    Demand represents the base electric load in the scheduling problem.

    Attributes:
    -----------
    uid:   Load unique id
    name:  Load name
    loads: List of load values [KW]
    """

    uid: int = -1
    name: str = ''
    loads: List[float] = field(default_factory=list)