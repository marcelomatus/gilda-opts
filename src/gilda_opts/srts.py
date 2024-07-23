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
    """
    SRTS represents the Simple Building Thermal Model load in the scheduling problem.

    Attributes:
     uid:  SRTS unique id
     name: SRTS name
     single_room:              SingleRoom instance
     min_temperature_sched:    Minimum temperature sched [C]
     max_temperature_sched:    Maximum temperature sched [C]
     thermal_drift_cost_sched: Thermal drift cost sched [$/C h]
    """

    uid: int = -1
    name: str = ""

    single_room: SingleRoom = field(default_factory=SingleRoom)

    min_temperature_sched: NumberSched = MIN_TEMPERATURE
    max_temperature_sched: NumberSched = MAX_TEMPERATURE
    thermal_drift_cost_sched: NumberSched = TEMPERATURE_DRIFT_COST


#  LocalWords:  uid SRTS SingleRoom
