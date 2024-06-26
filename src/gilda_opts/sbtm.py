"""SBTM module represents a Simple Building Thermal Model."""

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class SBTM(DataClassJsonMixin):
    """
    SBTM represents the Simple Building Thermal Model load in the scheduling problem.

    Attributes:
    -----------
    uid:          SBTM unique id
    name:         SBTM name
    bus_id:       Bus uid to be connected to
    """

    uid: int = -1
    name: str = ''
    bus_uid: int = -1
