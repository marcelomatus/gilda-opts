"""block module contains the time blocks used in the schedule problem formulation."""

from dataclasses import dataclass

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class Block(BaseClassJson):
    """Block represent time blocks used in the schedule problem formulation."""
    
    #: Block time duration [hours]
    duration: float = 1.0

    #: Discount factor to be used in the LP formulation
    discount: float = 1.0

    #: Integer variable type= 1:integers, 0: reals
    intvar_type: int = 1

    def energy_cost(self, cost):
        """Return energy cost value, which depends of the block duration."""
        return self.duration * self.power_cost(cost)

    def power_cost(self, cost):
        """Return the power cost value."""
        return cost * self.discount
