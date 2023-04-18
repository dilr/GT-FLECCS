"""
Modeling module
Declare PCC-related constraints.

Pengfei Cheng

1. PCC CO2 capture
2. PCC CO2 outlet concentration
3. PCC steam usage
4. PCC power usage
"""

from pyomo.environ import *
from ..pyomo_model.params import *
from .disaggregated_constraints import tCO2_flue



    # 1. PCC CO2 CAPTURE
    #def eq_PCC_CO2_cap(m, i):
    #    return m.x_CO2_PCC[i] == a_CO2_PCC * m.x_CO2_flue[i]
    #m.eq_PCC_CO2_cap = Constraint(set_hour_0, rule=eq_PCC_CO2_cap)
#TODO: allow dispatch
def tCO2_PCC(tfake_load):
    return a_CO2_PCC * tCO2_flue(tfake_load, 1)

    # --------------------------------------------------------------------------

    # 2. PCC CO2 OUTLET CONCENTRATION
    #def eq_PCC_CO2_out(m, i):
    #    return m.x_CO2_vent_PCC[i] == m.x_CO2_flue[i] - m.x_CO2_PCC[i]
    #m.eq_PCC_CO2_out = Constraint(set_hour_0, rule=eq_PCC_CO2_out)
def tCO2_vent_PCC(tfake_load):
    return tCO2_flue(tfake_load, 1) - tCO2_PCC(tfake_load)

    # --------------------------------------------------------------------------

    # 3. PCC STEAM USAGE
    #def eq_PCC_steam(m, i):
    #    return m.x_steam_PCC[i] == a_steam_PCC * m.x_CO2_PCC[i]
    #m.eq_PCC_steam = Constraint(set_hour_0, rule=eq_PCC_steam)
def tsteam_PCC(tfake_load):
    return a_steam_PCC * tCO2_PCC(tfake_load)

    # --------------------------------------------------------------------------

    # 4. PCC POWER USAGE
    #def eq_PCC_power(m, i):
    #    return m.x_power_PCC[i] == a_power_PCC * m.x_CO2_PCC[i]
    #m.eq_PCC_power = Constraint(set_hour_0, rule=eq_PCC_power)
def tpower_PCC(tfake_load):
    return a_power_PCC * tCO2_PCC(tfake_load)

