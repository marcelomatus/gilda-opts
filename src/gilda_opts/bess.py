"""BESS module represents a Battery Energy Storage System."""

from dataclasses import dataclass
from gilda_opts.battery import Battery


@dataclass
class BESS(Battery):
    """BESS represents a Battery Energy Storage System."""

    #: BESS unique id
    uid: int = -1

    #: BESS name
    name: str = ""

    #: Bus uid to be connected to
    bus_uid: int = -1
