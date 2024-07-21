"""Thermal unit module."""

from dataclasses import dataclass


from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched, IntSched, get_value_at


@dataclass
class ThermalUnit(BaseClassJson):
    """Thermal Unit.

    capacity:    Electric capacity [KW]
    efficiency:  Efficiency KW heat/ KWh electricity [0..1]

    uid:             ThermalUnit unique id
    name:            ThermalUnit name
    bus_uid:         Bus uid to be connected to
    srts_uid:        SRTS uid to be attached to

    electric_capacity:  electric consumption capacity [KW]
    thermal_capacity:   thermal capacity [KW]
    thermal_cost:       thermal cost additional to the electricity cost [$/KWh]
    heating_efficiency: how much thermal energy is transferred to the room [0..1]
    cooling_efficiency: how much thermal energy is transferred to the room [0..1]

    active_mode:        active mode list: 1: heating, 0: disconnected, -1: cooling
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1
    srts_uid: int = -1

    capacity: float = 0
    heating_efficiency: float = 0
    cooling_efficiency: float = 0

    thermal_capacity: float = 0
    thermal_cost: NumberSched = 0
    active_mode: IntSched = 1

    def get_thermal_capacity(self, bid: int):
        """Return thermal capacity."""
        active_mode = get_value_at(self.active_mode, bid, 0)
        if active_mode == 0:
            return 0, 0, 0

        efficiency = (
            self.heating_efficiency if active_mode > 0 else self.cooling_efficiency
        )

        thermal_capacity = efficiency * self.capacity + self.thermal_capacity
        thermal_cost = get_value_at(self.thermal_cost, bid, 0) * self.thermal_capacity
        return thermal_capacity, thermal_cost, active_mode


#  LocalWords: SRTS uid srts
