"""Demand module represents a base electric load."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class Demand(BaseClassJson):
    """Demand represents the base electric load in the scheduling problem."""
    
    #: Load unique id
    uid: int = -1

    #: Load name
    name: str = ""

    #: Bus uid to be connected to
    bus_uid: int = -1

    #: Load schedule [KW]
    load_sched: NumberSched = 0.0

    #: Cost of fail to schedule load
    cfail_sched: NumberSched = -1
