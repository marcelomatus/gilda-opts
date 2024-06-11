"""block module contains the time blocks used in the schedule problem formulation."""

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Block(DataClassJsonMixin):
    """
    Block represent time blocks used in the schedule problem formulation.

    Attribute:
    ----------
    duration: Block time duration [hours]
    index: Block time index, when is part of a time series [0..Inf]
    """

    duration: float = 0
    index: int = -1
    discount: float = 1.0
