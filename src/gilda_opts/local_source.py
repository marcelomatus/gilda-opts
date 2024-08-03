"""LocalSource module contains the basic local energy source, such as PV or Wind."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class LocalSource(BaseClassJson):
    """A LocalSource refers to a local electric power source.

    The main local sources include solar panels and small wind turbines for home.

    This local renewable generation is quantified in megawatts (MW) of capacity"""

    #: LocalSource unique id
    uid: int = -1

    #: LocalSource provider name
    name: str = ""

    #: Bus uid
    bus_uid: int = -1

    #: Connection Capacity [KW]
    capacity: float = 0

    #: Generation profile, as a factor of the  capacity [0..1]
    generation_profile_sched: NumberSched = 0
