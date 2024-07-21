"""Demand module represents a base electric load."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class Demand(BaseClassJson):
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
    name: str = ""
    bus_uid: int = -1
    loads: NumberSched = 0.0
    cfail: float = -1
