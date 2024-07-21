"""block module contains the time blocks used in the schedule problem formulation."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class Block(BaseClassJson):
    """
    Block represent time blocks used in the schedule problem formulation.

    Attribute:
    ----------
    duration: Block time duration [hours]
    discount: Discount factor to be used in the LP formulation
    intvar_type:  Integer variable type= 1:integers, 0: reals
    """

    duration: float = 1.0
    discount: float = 1.0
    intvar_type: int = 1

    def energy_cost(self, cost):
        """Return energy cost value, which depends of the block duration."""
        return self.duration * self.power_cost(cost)

    def power_cost(self, cost):
        """Return the power cost value."""
        return cost * self.discount
