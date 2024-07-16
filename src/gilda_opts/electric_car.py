"""ElectricCar module represents an Electric Car."""

from dataclasses import dataclass, field
from typing import List
from gilda_opts.baseclass_json import BaseClassJson

ATHOME_MASK = 0
ONROAD_MASK = 1
PLUGGED_MASK = 2


@dataclass
class ElectricCar(BaseClassJson):
    """
    ElectricCar represents an Electric Car.

    Attributes:
    -----------
    uid:                    ElectricCar unique id
    name:                   ElectricCar name
    athome_bus_uid:         Bus uid to be connected to at home
    charger_bus_uid:        Bus uid to be connected to on public charger

    battery_capacity:       Storage capacity [KWh]
    battery_max_flow:       Max charging & discharging flow [KW]
    engine_max_flow:        Max engine flow [KW]
    battery_efficiency:     In & Out efficiency [0..1]
    battery_initial_charge: Initial charge [KWh]
    battery_final_charge:     Final charge [KWh]
    battery_replacement_cost: Net cost of battery replacement at the end of CL [$/KWh]
    battery_cycle_life:      Number of cycles before battery replacement [N]

    location_masks:         at_home=0, on_street=1,2,4,...
    onroad_distances:       Traveled distances while on the street [Km]
    energy_consumption      energy_consumption [Kwh/Km]
    """

    uid: int = -1
    name: str = ""
    athome_bus_uid: int = -1
    public_bus_uid: int = -1

    battery_capacity: float = 0
    battery_max_flow: float = 0
    battery_efficiency: float = 0
    battery_initial_charge: float = 0
    battery_final_charge: float = 0
    battery_discharge_cost: float = 0
    battery_cycle_life: float = 10000
    battery_replacement_cost: float = 100

    engine_max_float: float = float("inf")

    energy_consumption: float = 0
    location_masks: List[int] = field(default_factory=list)
    onroad_distances: List[float] = field(default_factory=list)
