"""LocalSource module contains the basic local energy source, such as PV or Wind."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class LocalSource(BaseClassJson):
    """
    A LocalSource represents a local energy source .

    Attributes:
    ----------
    uid:                LocalSource unique id
    name:               LocalSource provider name
    capacity:           Connection Capacity [KW]
    generation_profile_sched: Potential generation profile schedule, as a factor of the
                        capacity [0..1]
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1
    capacity: float = 0
    generation_profile_sched: NumberSched = 0
