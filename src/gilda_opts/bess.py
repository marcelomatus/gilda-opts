"""BESS module represents a Battery Energy Storage System."""

from dataclasses import dataclass
from gilda_opts.battery import Battery


@dataclass
class BESS(Battery):
    """Battery energy storage systems(BESS), allow energy generated from renewable sources such as solar and wind to be stored 
    and later used during periods of high demand , helping to reduce costs and ensure a continuous electricity supply.
    
    BESS are significantly more sophisticated than typical batteries. Advanced software algorithms manage energy production, 
    while computerized control systems determine the optimal times to store or release energy to the grid. """

    #: BESS unique id
    uid: int = -1

    #: BESS name
    name: str = ""

    #: Bus uid to be connected to
    bus_uid: int = -1
