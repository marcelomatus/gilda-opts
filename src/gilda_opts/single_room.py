"""SingleRoom module."""

from dataclasses import dataclass
from math import sqrt

from gilda_opts.baseclass_json import BaseClassJson
from gilda_opts.utils import NumberSched


@dataclass
class SingleRoom(BaseClassJson):
    """
    SingleRoom represents single room.

    Attributes:
     total_floor_area:            area                                 [m2]
     height:                      height                               [m]
     u_value:                     U-value (thermal transmittance)      [W/m2 K]
     air_renewal:                 Air renewals per hour                [1/h]
     air_density:                 Air density                          [kg/m3]
     air_specific_heat_capacity:  Specific heat capacity of air        [kJ/kg K]
     thermal_mass_parameter:      Thermal mass parameter (kappa value) [kJ/m2K]
     initial_temperature:         Initial temperature                  [C]
     external_temperature_sched:  External temperature                 [C]
     external_heating_sched:      External heating (ie, sun + occupancy)  [KW]
    """

    total_floor_area: float = 70
    height: float = 2.5
    u_value: float = 2
    air_renewal: float = 0.5
    air_density: float = 1.225
    air_specific_heat_capacity: float = 1.005
    thermal_mass_parameter: float = 250.0
    initial_temperature: float = 20

    external_temperature_sched: NumberSched = 20
    external_heating_sched: NumberSched = 0

    #
    # public methods
    #
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
        d_t = duration * 3600

        tmp = self.thermal_mass_parameter
        u = self.u_value / 1000.0
        ach = self.air_renewal
        rho_air = self.air_density
        c_air = self.air_specific_heat_capacity
        tfa = self.total_floor_area
        height = self.height
        esa = 4 * sqrt(tfa) * height + 2 * tfa
        room_vol = tfa * height

        convective_loss = ach * room_vol * rho_air * c_air / 3600.0
        conductive_loss = esa * u
        return d_t * (convective_loss + conductive_loss) / (tmp * tfa)

    def q_coeff(self, duration: float, thermal_capacity):
        """Return the thermal unit Q coefficient."""
        #  Thermal unit q coeff
        #      P_e * D_t / ( TMP * TFA )
        #
        d_t = duration * 3600

        p_i = thermal_capacity
        tmp = self.thermal_mass_parameter
        tfa = self.total_floor_area

        return d_t * p_i / (tmp * tfa)
