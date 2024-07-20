"""SBTM module represents a Simple Building Thermal Model."""

from dataclasses import dataclass, field
from math import sqrt

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class ThermalUnit(BaseClassJson):
    """heating Unit.

    capacity:    Electric capacity [KW]
    efficiency:  Efficiency KW heat/ KWh electricity [0..1]
    """

    capacity: float = 0
    efficiency: float = 0


@dataclass
class SingleRoom(BaseClassJson):
    """
    SingleRoom represents a .

    Attributes:
    -----------
    total_floor_area:            area                                 m2
    height:                      height                               m
    u_value:                     U-value (thermal transmittance)      W/m2K
    air_renewal:                 Air renewals per hour                1/h
    air_density:                 Air density                          kg/m3
    air_specific_heat_capacity:  Specific heat capacity of air        kJ/kg K
    thermal_mass_parameter:      Thermal mass parameter (kappa value) kJ/m2K
    heating_power:               Heating power                        kW
    time_interval:               Time interval                        s
    initial_temperature:         Initial temperature                  C
    external_temperatures:       External temperature                 C
    thermal_drift_cost:          Thermal drift cost                   $/C h
    """

    total_floor_area: float = 70
    height: float = 2.5
    u_value: float = 2
    air_renewal: float = 0.5
    air_density: float = 1.225
    air_specific_heat_capacity: float = 1.005
    thermal_mass_parameter: float = 250.0
    heating_power: float = 10
    time_interval: float = 1800
    initial_temperature: float = 20
    external_temperatures: NumberSched = 20
    thermal_drift_cost: NumberSched = 120000 / (20 * 24)

    def temperature_coeff(self):
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
        return (convective_loss + conductive_loss) / (TMP * TFA)

    def q_coeff(self, thermal_unit: ThermalUnit):
        """Return the thermal unit Q coefficient."""
        #  Thermal unit q coeff
        #      n_t * P_e * D_t / ( TMP * TFA )
        #
        if thermal_unit is None:
            return 0

        n_i = thermal_unit.efficiency
        P_i = thermal_unit.capacity  # pylint: disable=C0103
        TMP = self.thermal_mass_parameter  # pylint: disable=C0103
        TFA = self.total_floor_area  # pylint: disable=C0103

        return n_i * P_i / (TMP * TFA)


@dataclass
class SBTM(BaseClassJson):
    """
    SBTM represents the Simple Building Thermal Model load in the scheduling problem.

    Attributes:
    -----------
    uid:             SBTM unique id
    name:            SBTM name
    bus_uid:         Bus uid to be connected to

    min_temperature: minimum temperature
    max_temperature: maximum temperature
    """

    uid: int = -1
    name: str = ""
    bus_uid: int = -1

    single_room: SingleRoom = field(default_factory=SingleRoom)
    heating_unit: ThermalUnit = field(default_factory=ThermalUnit)
    cooling_unit: ThermalUnit = field(default_factory=ThermalUnit)

    min_temperature: NumberSched = 20
    max_temperature: NumberSched = 20
