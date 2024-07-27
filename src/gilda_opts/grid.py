"""Grid module contains the basic grid electric provider."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class Grid(BaseClassJson):
    """A Grid represents the electric service from the grid company."""

    #: Grid unique id
    uid: int = -1
    #: Grid provider name
    name: str = ""
    #: Bus uid
    bus_uid: int = -1

    #: Connection Capacity [KW]
    capacity: float = 0
    #: Withdrawn profile schedule, as a factor of capacity [0..1]
    withdrawn_profile_sched: NumberSched = 1.0
    #: Injection profile schedule, as a factor of capacity [0..1]
    injection_profile_sched: NumberSched = 1.0

    #: Energy tariff schedule (withdrawn) [$/KWh]
    energy_buy_price_sched: NumberSched = 0.0
    #: Energy sell price schedule (injection) [$/KWh]
    energy_sell_price_sched: NumberSched = 0.0

    #: Emission cost [$/gCO2]
    emission_cost: float = 0.0
    #: Emission factor schedule [gCO2/KWh]
    emission_factor_sched: NumberSched = 0.0

    #: Power tariff [$/KW]
    power_tariff: float = 0.0
    #: Power factor schedule [0..1]
    power_factor_sched: NumberSched = 0.0
