"""Thermal unit module."""

from dataclasses import dataclass


from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched, IntSched, get_value_at

HEATING_MODE = +1
COOLING_MODE = -1
OFFLINE_MODE = 0


@dataclass
class ThermalUnit(BaseClassJson):
    """Thermal Unit."""

    #: ThermalUnit unique id
    uid: int = -1
    #: ThermalUnit name
    name: str = ""
    #: Bus uid to be connected electrically
    bus_uid: int = -1
    #: SRTS uid to be attached thermally
    srts_uid: int = -1

    #: Electric capacity [KW]
    capacity: float = 0
    #: How much electric energy is converted to heating [0..1]
    heating_efficiency: float = 0
    #: How much electric energy is converted to cooling [0..1]
    cooling_efficiency: float = 0

    #: Thermal capacity additional to the electrical energy [KW]
    thermal_capacity: float = 0
    #: Thermal cost additional to the electricity cost [$/KWh]
    thermal_cost_sched: NumberSched = 0

    #: Is the on/off state:  binary=0 or continuous=1 [0,1]
    power_controlled: int = 0
    #: Active mode sched: 1= heating, 0= offline, -1= cooling [-1,0,1]
    active_mode_sched: IntSched = 1

    #
    # public methods
    #
    def get_thermal_parameters(self, bid: int):
        """Return thermal capacity, thermal_cost and active_mode."""
        active_mode = get_value_at(self.active_mode_sched, bid, OFFLINE_MODE)
        if active_mode == OFFLINE_MODE:
            return 0, 0, active_mode

        efficiency = (
            self.heating_efficiency
            if active_mode == HEATING_MODE
            else self.cooling_efficiency
        )

        thermal_capacity = efficiency * self.capacity + self.thermal_capacity
        thermal_cost = (
            get_value_at(self.thermal_cost_sched, bid, 0) * self.thermal_capacity
        )
        return thermal_capacity, thermal_cost, active_mode


#  LocalWords: SRTS uid srts ThermalUnit
