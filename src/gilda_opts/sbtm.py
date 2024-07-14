"""SBTM module represents a Simple Building Thermal Model."""

from dataclasses import dataclass
from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class SBTM(BaseClassJson):
    """
    SBTM represents the Simple Building Thermal Model load in the scheduling problem.

    Attributes:
    -----------
    uid:          SBTM unique id
    name:         SBTM name
    bus_uid:      Bus uid to be connected to
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1
