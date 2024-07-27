"""ElectricCar module represents an Electric Car."""

from dataclasses import dataclass, field

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.battery import Battery
from gilda_opts.utils import IntSched, NumberSched


def default_battery():
    """Return the default battery for an electric_car."""
    return Battery(
        capacity=50,
        max_flow_in=50,
        max_flow_out=0,
        efficiency_in=0.95,
        efficiency_out=0.95,
        emin_profile_sched=0.2,
        emax_profile_sched=0.9,
    )


@dataclass
class Engine(BaseClassJson):
    """Engine represetns an Electric Engine."""
    
    #: Energy efficiency [Km/Kwh]
    energy_efficiency: float = 8.0


@dataclass
class ElectricCar(BaseClassJson):
    """ElectricCar represents an Electric Car."""
    
    #: ElectricCar unique id
    uid: int = -1
    #: ElectricCar name
    name: str = ""

    #: Storage system [Battery]    
    battery: Battery = field(default_factory=default_battery)
    #: Electric engine [Engine]
    engine: Engine = field(default_factory=Engine)

    #: Bus_id where is plugged or unplugged=-1
    bus_uid_sched: IntSched = -1
    #: Traveled distances while on road [Km]
    distance_sched: NumberSched = 0
    #: Fail distance cost, you may use the taxi tariff [$/Km]
    cfail_sched: NumberSched = -1
