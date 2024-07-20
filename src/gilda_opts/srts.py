"""SRTS module represents a Simple Building Thermal Model."""

from dataclasses import dataclass, field
from math import sqrt

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched
from gilda_opts.thermal_unit import ThermalUnit


@dataclass
class SingleRoom(BaseClassJson):
    """
    SingleRoom represents single room.

    Attributes:
    -----------
    total_floor_area:            area                                 m2
    height:                      height                               m
    u_value:                     U-value (thermal transmittance)      W/m2K
    air_renewal:                 Air renewals per hour                1/h
    air_density:                 Air density                          kg/m3
    air_specific_heat_capacity:  Specific heat capacity of air        kJ/kg K
    thermal_mass_parameter:      Thermal mass parameter (kappa value) kJ/m2K
    initial_temperature:         Initial temperature                  C
    external_temperatures:       External temperature                 C
    """

    total_floor_area: float = 70
    height: float = 2.5
    u_value: float = 2
    air_renewal: float = 0.5
    air_density: float = 1.225
    air_specific_heat_capacity: float = 1.005
    thermal_mass_parameter: float = 250.0
    initial_temperature: float = 20
    external_temperatures: NumberSched = 20

    def temperature_coeff(self, duration: float):
        """Return the temperature coefficient."""
        #
        #  Temperature Coefficient
        #    1.0 / ( TMP * TFA ) * (ACH * RoomVol * Rho_air * C_air / 3600 + ESA
        #
        #      TMP = kappa
        #      RoomVol = area * height
        #      ESA = 4 * sqrt(area) * height + 2 * area
        #      TFA = area
        #
        D_t = duration * 3600  # pylint: disable=C0103

        TMP = self.thermal_mass_parameter  # pylint: disable=C0103
        U = self.u_value / 1000.0  # pylint: disable=C0103
        ACH = self.air_renewal  # pylint: disable=C0103
        Rho_air = self.air_density  # pylint: disable=C0103
        C_air = self.air_specific_heat_capacity  # pylint: disable=C0103
        TFA = self.total_floor_area  # pylint: disable=C0103
        height = self.height  # pylint: disable=C0103
        ESA = 4 * sqrt(TFA) * height + 2 * TFA  # pylint: disable=C0103
        RoomVol = TFA * height  # pylint: disable=C0103

        convective_loss = ACH * RoomVol * Rho_air * C_air / 3600.0
        conductive_loss = ESA * U
        return D_t * (convective_loss + conductive_loss) / (TMP * TFA)

    def q_coeff(self, duration: float, thermal_capacity):
        """Return the thermal unit Q coefficient."""
        #  Thermal unit q coeff
        #      n_t * P_e * D_t / ( TMP * TFA )
        #
        D_t = duration * 3600  # pylint: disable=C0103

        P_i = thermal_capacity  # pylint: disable=C0103
        TMP = self.thermal_mass_parameter  # pylint: disable=C0103
        TFA = self.total_floor_area  # pylint: disable=C0103

        return D_t * P_i / (TMP * TFA)


@dataclass
class SRTS(BaseClassJson):
    """
    SRTS represents the Simple Building Thermal Model load in the scheduling problem.

    Attributes:
    -----------
    uid:  SRTS unique id
    name: SRTS name

    min_temperature:    Minimum temperature [C]
    max_temperature:    Maximum temperature [C]
    thermal_drift_cost: Thermal drift cost [$/C h]
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1

    single_room: SingleRoom = field(default_factory=SingleRoom)
    heating_unit: ThermalUnit = field(default_factory=ThermalUnit)
    cooling_unit: ThermalUnit = field(default_factory=ThermalUnit)

    min_temperature: NumberSched = 20
    max_temperature: NumberSched = 20
    thermal_drift_cost: NumberSched = 160000 / (20 * 8)


#  LocalWords:  IntSched uid
