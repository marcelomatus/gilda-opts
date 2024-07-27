"""Line module represents a line between two buses."""

from dataclasses import dataclass


from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class Line(BaseClassJson):
    """Line represents a line between two buses."""

    #: Line unique id
    uid: int = -1
    #: Line name
    name: str = ""
    #: Bus a uid to be connected
    bus_a_uid: int = -1
    #: Bus b uid to be connected
    bus_b_uid: int = -1

    #: Transmission capacity [KW]
    capacity: float = 0
    #: Max flow profile sched [0..1]
    max_flow_profile_sched: NumberSched = 1
    #: Max flow profile sched [0..1]
    min_flow_profile_sched: NumberSched = -1

    #: line losses
    losses: float = 0
