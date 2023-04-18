"""
Modeling module
Constraints related to DAC costing.

Pengfei Cheng
2022
"""

from pyomo.environ import *
from ..pyomo_model.params import *


    # calculate the cost of sorbent
    #def eq_cost_sorbent(m):
    #    return m.x_cost_sorbent == a_cost_sorbent * m.x_sorbent_total
    #m.eq_cost_sorbent = Constraint(rule=eq_cost_sorbent)
def cost_sorbent(sorbent_total):
    return a_cost_sorbent * sorbent_total

    # volume of blown air
    #def eq_adsorb_air_volume(m, i, j):
    #    return m.x_air_adsorb[i, j] >= (m.x_sorbent_A0[i, j] + m.x_sorbent_A1[i, j]) * sorbent_cap_DAC_air / 2 * tonne_to_g / CO2_mole_w * mole_vol / CO2_vol_ratio                                 # m^3 air
    #m.eq_adsorb_air_volume = Constraint(set_hour_0, set_quarter, rule=eq_adsorb_air_volume)
def dair_adsorb(dsorbent_A):
    return dsorbent_A * sorbent_cap_DAC_air / 2 * tonne_to_g / CO2_mole_w * mole_vol / CO2_vol_ratio

    #TODO: move to constraints
    # max adsorption air rate
    #def eq_adsorb_max_air_rate(m, i, j):
    #    return m.x_air_adsorb_max >= m.x_air_adsorb[i, j] / 15 / 60  # 1 slice = 15 min = 900 s
    #m.eq_adsorb_max_air_rate = Constraint(set_hour_0, set_quarter, rule=eq_adsorb_max_air_rate)

    # calculate the cost of adsorption systems
    #def eq_cost_adsorption_sys(m):
    #    return m.x_cost_adsorb == a_cost_adsorb * m.x_air_adsorb_max
    #m.eq_cost_adsorption_sys = Constraint(rule=eq_cost_adsorption_sys)
def cost_adsorb(air_adsorb_max):
    return a_cost_adsorb * air_adsorb_max

    # calculate the total capital cost of DAC systems
    #def eq_capital_cost_DAC(m):
    #    return m.x_cost_DAC_TPC == m.x_cost_sorbent + m.x_cost_adsorb
    #m.eq_capital_cost_DAC = Constraint(rule=eq_capital_cost_DAC)
def cost_DAC_TPC(air_adsorb_max, sorbent_total):
    return cost_sorbent(sorbent_total) + cost_adsorb(air_adsorb_max)
