"""BESS module represents a Battery Energy Storage System."""

from dataclasses import dataclass
from typing import Any

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class Battery(BaseClassJson):
    """
    Battery represents a Battery Element.

    Attributes:
    -----------
    uid:          BESS unique id
    name:         BESS name
    bus_uid:       Bus uid to be connected to
    capacity:     Storage capacity [KWh]
    max_flow_in:   Max in  flow [KW]
    max_flow_out:  Max out flow [KW]
    efficiency:   In&Out efficiency [0..1]
    eini:         Start energy stored [KWh]
    efin:         End energy stored [KWh]
    efin_price:   Energy value at the end of the period [$/KWh]
    discharge_cost: Discharge cost, related to the replacement cost [$/KWh]
    emin_profile:  Minimum energy as proportion of the capacity [0..1]
    emax_profile:  Maximum energy as proportion of the capacity [0..1]
    """

    capacity: float = 0
    max_flow_in: float = 0
    max_flow_out: float = 0
    efficiency_in: float = 1
    efficiency_out: float = 1
    eini: float = 0
    efin: float = 0
    efin_price: float = 0
    discharge_cost: float = 0
    emin_profile: Any = 0
    emax_profile: Any = 1


@dataclass
class BESS(Battery):
    """
    BESS represents a Battery Energy Storage System.

    Attributes:
    -----------
    uid:          BESS unique id
    name:         BESS name
    bus_uid:       Bus uid to be connected to
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1
