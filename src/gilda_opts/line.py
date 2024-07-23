"""Line module represents a line between two buses."""

from dataclasses import dataclass


from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class Line(BaseClassJson):
    """Line represents a line between two buses.

    Attributes:
     uid:          Line unique id
     name:         Line name
     bus_a_uid:    Bus a uid to be connected
     bus_b_uid:    Bus b uid to be connected
     capacity:     Transmission capacity [KW]
     max_flow_profile_sched:  Max flow profile sched [0..1]
     min_flow_rpofile_sched:  Max flow profile sched [0..1]
    """

    uid: int = -1
    name: str = ""
    bus_a_uid: int = -1
    bus_b_uid: int = -1

    capacity: float = 0
    max_flow_profile_sched: NumberSched = 1
    min_flow_profile_sched: NumberSched = -1

    losses: float = 0
