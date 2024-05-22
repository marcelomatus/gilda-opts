"""Demand class to represent a base electric load."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class Demand(DataClassJsonMixin):
    """Demand class."""

    uid: int = -1
    name: str = ''
    loads: List[float] = field(default_factory=list)
