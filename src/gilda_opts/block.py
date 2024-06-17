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
    discount: Discount factor to be used in the LP formulation
    """

    duration: float = 1.0
    discount: float = 1.0
