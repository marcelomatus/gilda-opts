"""Grid module contains the basic grid electric provider."""

from dataclasses import dataclass, field
from typing import List, Any

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class Grid(BaseClassJson):
    """
    A Grid represents the electric service from the grid company.

    Attributes:
    ----------
    uid:              Grid unique id
    name:             Grid provider name
    capacity:         Connection Capacity [KW]
    withdrawn_profile: Withdrawn profile value, as a factor of the capacity [0..1]
    injection_profile: Injection profile value, as a factor of the capacity [0..1]
    energy_tariffs:   List of energy buy(withdrawn) tariff values [$/KWh]
    power_tariff:     Power tariff [$/KW]
    power_factors:    List of power factor values [0..1]
    emission_factors: List of emission factors [gCO2/KWh]
    emission_cost:    Emission cost [$/gCO2]
    energy_sell_prices:    Energy sell(injection) price [$/KWh]
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1
    capacity: float = 0
    withdrawn_profile: List[float] = field(default_factory=list)
    injection_profile: List[float] = field(default_factory=list)
    energy_tariffs: List[float] = field(default_factory=list)
    power_tariff: float = 0
    power_factors: Any = None
    emission_factors: List[float] = field(default_factory=list)
    emission_cost: float = 0
    energy_sell_prices: List[float] = field(default_factory=list)
