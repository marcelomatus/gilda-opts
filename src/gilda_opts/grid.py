"""Grid module contains the basic grid electric provider."""

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class Grid(DataClassJsonMixin):
    """
    A Grid represents the electric service from the grid company.

    Attributes:
    ----------
    uid:              Grid unique id
    name:             Grid provider name
    capacity:         Connection Capacity [KW]
    energy_tariffs:   List of energy tariff values [$/KWh]
    power_tariff:     Power tariff [$/KW]
    power_factors:    List of power factor values [0..1]
    emission_factors: List of emission factors [gCO2/KWh]
    emission_cost:    Emission cost [$/gCO2]
    """

    uid: int = -1
    name: str = ''
    bus_uid: int = -1
    capacity: float = 0
    energy_tariffs: List[float] = field(default_factory=list)
    power_tariff: float = 0
    power_factors: List[float] = field(default_factory=list)
    emission_factors: List[float] = field(default_factory=list)
    emission_cost: float = 0
