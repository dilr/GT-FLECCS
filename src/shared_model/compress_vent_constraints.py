"""
Modeling module
Declare compressor and vented CO2-related constraints.

Pengfei Cheng

1. CO2 compression amount
2. power usage of CO2 compression
3. total CO2 captured
"""


from pyomo.environ import *
from ..pyomo_model.params import *
from .PCC_constraints import tCO2_PCC, tCO2_vent_PCC
from .DAC_constraints import dCO2_DAC


    # 1. CO2 compression amount
    ## integral over all slices within each hour
    #def eq_compress_CO2(m, i):
    #    return m.x_CO2_compress[i] == m.x_CO2_PCC[i] + sum(m.x_CO2_DAC[i, j] for j in set_quarter)
    #m.eq_compress_CO2 = Constraint(set_hour_0, rule=eq_compress_CO2)
def tCO2_compress(tfake_load):
    return tCO2_PCC(tfake_load)
def dCO2_compress(dsorbent_A):
    return dCO2_DAC(dsorbent_A)

    # --------------------------------------------------------------------------

    # 2. power usage of CO2 compression
    #def eq_compress_CO2_power(m, i):
    #    return m.x_power_compress[i] == a_power_compr_PCC * m.x_CO2_PCC[i] + a_power_compr_DAC * sum(m.x_CO2_DAC[i, j] for j in set_quarter)
    #m.eq_compress_CO2_power = Constraint(set_hour_0, rule=eq_compress_CO2_power)
def tpower_compress(tfake_load):
    return a_power_compr_PCC * tCO2_PCC(tfake_load)
def dpower_compress(dsorbent_A):
    return a_power_compr_DAC * dCO2_DAC(dsorbent_A)

    # --------------------------------------------------------------------------

    # 2. power usage of CO2 compression
    #def eq_CO2_cap_total(m, i):
    #    return m.x_CO2_cap_total[i] == - m.x_CO2_vent_PCC[i] + (1 - a_CO2_vent_DAC) * sum(m.x_CO2_DAC[i, j] for j in set_quarter)
    #m.eq_CO2_cap_total = Constraint(set_hour_0, rule=eq_CO2_cap_total)
def tCO2_cap_total(tfake_load):
    return - tCO2_vent_PCC(tfake_load)
def dCO2_cap_total(dsorbent_A):
    return  (1 - a_CO2_vent_DAC) * dCO2_DAC(dsorbent_A)
