"""Battery module represents a Battery Energy Storage System."""

from dataclasses import dataclass
from gilda_opts.utils import NumberSched

from gilda_opts.baseclass_json import BaseClassJson


@dataclass
class Battery(BaseClassJson):
    """Battery represents an electric battery Element."""

    #: Storage capacity [KWh]
    capacity: float = 0
    #: Max flow, it will apply to both in/out if not provided [KW]
    max_flow: float = 0
    #: Max flow in [KW]
    max_flow_in: float = -1
    #: Max flow out [KW]
    max_flow_out: float = -1
    #: In/Out efficiency [0..1]
    efficiency: float = 1
    #: In efficiency [0..1]
    efficiency_in: float = -1
    #: Out efficiency [0..1]
    efficiency_out: float = -1
    #: Initial energy stored [KWh]
    eini: float = 0
    #: finale energy stored [KWh]
    efin: float = 0
    #: Energy value at the end of the period [$/KWh]
    efin_price: float = 0
    #: Discharge cost, related to the replacement cost [$/KWh]
    discharge_cost: float = 0
    #: Minimum energy as proportion of the capacity [0..1]
    emin_profile_sched: NumberSched = 0
    #: Maximum energy as proportion of the capacity [0..1]
    emax_profile_sched: NumberSched = 1

    #
    # public methods
    #

    def get_max_flow_in(self):
        """Return the max_flow_in.

        :meta private:
        """
        return self.max_flow_in if self.max_flow_in >= 0 else self.max_flow

    def get_max_flow_out(self):
        """Return the max_flow_out.

        :meta private:
        """
        return self.max_flow_out if self.max_flow_out >= 0 else self.max_flow

    def get_efficiency_in(self):
        """Return the efficiency.

        :meta private:
        """
        return self.efficiency_in if self.efficiency_in >= 0 else self.efficiency

    def get_efficiency_out(self):
        """Return the efficiency.

        :meta private:
        """
        return self.efficiency_out if self.efficiency_out >= 0 else self.efficiency
