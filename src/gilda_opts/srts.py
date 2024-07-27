"""SRTS module represents a Simple Building Thermal Model."""

from dataclasses import dataclass, field

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched
from gilda_opts.single_room import SingleRoom

MIN_TEMPERATURE = -20
MAX_TEMPERATURE = 50
TEMPERATURE_DRIFT_COST = 160000.0 / (20 * 8)


@dataclass
class SRTS(BaseClassJson):
    """SRTS represents the Simple Building Thermal Model load in the scheduling problem."""

    #: SRTS unique id
    uid: int = -1
    #: SRTS name
    name: str = ""

    #: SingleRoom instance
    single_room: SingleRoom = field(default_factory=SingleRoom)

    #: Minimum temperature sched [C]
    min_temperature_sched: NumberSched = MIN_TEMPERATURE
    #: Maximum temperature sched [C]
    max_temperature_sched: NumberSched = MAX_TEMPERATURE
    #: Thermal drift cost sched [$/C h]
    thermal_drift_cost_sched: NumberSched = TEMPERATURE_DRIFT_COST


#  LocalWords:  uid SRTS SingleRoom
