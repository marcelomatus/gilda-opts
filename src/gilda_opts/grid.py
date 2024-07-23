"""Grid module contains the basic grid electric provider."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class Grid(BaseClassJson):
    """
    A Grid represents the electric service from the grid company.

    Attributes:
     uid:              Grid unique id
     name:             Grid provider name
     bus_uid:          Bus uid
     capacity:                Connection Capacity [KW]
     withdrawn_profile_sched: Withdrawn profile schedule, as a factor of capacity [0..1]
     injection_profile_sched: Injection profile schedule, as a factor of capacity [0..1]
     energy_buy_price_sched:     Energy tariff schedule (withdrawn) [$/KWh]
     energy_sell_price_sched: Energy sell price schedule (injection) [$/KWh]
     power_tariff:       Power tariff [$/KW]
     power_factor_sched: Power factor schedule [0..1]
     emission_cost:         Emission cost [$/gCO2]
     emission_factor_sched: Emission factor schedule [gCO2/KWh]
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1

    capacity: float = 0
    withdrawn_profile_sched: NumberSched = 1.0
    injection_profile_sched: NumberSched = 1.0

    energy_buy_price_sched: NumberSched = 0.0
    energy_sell_price_sched: NumberSched = 0.0

    emission_cost: float = 0.0
    emission_factor_sched: NumberSched = 0.0

    power_tariff: float = 0.0
    power_factor_sched: NumberSched = 0.0
