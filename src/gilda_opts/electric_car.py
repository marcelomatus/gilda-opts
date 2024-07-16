"""ElectricCar module represents an Electric Car."""

from dataclasses import dataclass, field
from typing import List

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.bess import Battery


ATHOME_MASK = 0
ONROAD_MASK = 1
PLUGGED_MASK = 2


def default_battery():
    """Return the default battery for an electric_car."""
    return Battery(
        capacity=50,
        max_flow_in=50,
        max_flow_out=0,
        efficiency_in=0.95,
        emin_profile=0.2,
        emax_profile=0.9,
    )


@dataclass
class Engine(BaseClassJson):
    """
    Engine represetns an Electric Engine.

    Attributes:
    -----------
    energy_consumption:   Energy consumption [Kwh/Km]
    efficiency:           Transfer efficiency out of the battery to the engine [0..1]
    """

    energy_consumption: float = 0
    efficiency: float = 1


def default_engine():
    """Return the default battery for an electric_car."""
    return Engine(
        energy_consumption=1.0 / 6.0,
        efficiency=0.95,
    )


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

    battery:                Storage system [Battery]
    engine:        Electric engine [Engine]

    location_masks:         at_home=0, on_street=1,2,4,...
    onroad_distances:       Traveled distances while on the street [Km]
    """

    uid: int = -1
    name: str = ""
    athome_bus_uid: int = -1
    public_bus_uid: int = -1

    battery: Battery = field(default_factory=default_battery)
    engine: Engine = field(default_factory=default_engine)

    location_masks: List[int] = field(default_factory=list)
    onroad_distances: List[float] = field(default_factory=list)
