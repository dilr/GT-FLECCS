"""
Objective Module
Define the objective function.

Pengfei Cheng
2022
"""

from pyomo.environ import *
from .params import *

def obj_expr(m, cost_NG, CO2_CREDIT, power_price, cost_start_up, set_hour):
    return \
        ( sum(
             - cost_NG * m.x_fuel[i] + \
                CO2_CREDIT * m.x_CO2_cap_total[i] - \
                a_cost_CO2_TS * m.x_CO2_compress[i] + \
                power_price[i] * m.x_power_net[i] - \
                cost_start_up * m.z0[i] - \
                m.x_cost_NGCC_VOM[i] - m.x_cost_PCC_VOM[i] - m.x_cost_DAC_VOM[i] - m.x_cost_PCC_compr_VOM[i] - m.x_cost_DAC_compr_VOM[i]
            for i in set_hour) \
        - m.x_cost_DAC_FOM ) * (1 - tax_r) * sum(1 / (1 + int_r) ** j for j in range(2, 21 + 1)) \
        - m.x_cost_DAC_TPC * (1 + 0.0311 + 0.0066 + 0.1779) * ( 0.3 + 0.7 / (1 + int_r) - sum(tax_r * depreciate_r * ((1 - depreciate_r) ** j) * ((1 + int_r) ** (- j - 2)) for j in range(19 + 1)) )

def add_objective_function(m, cost_NG, CO2_CREDIT, power_price, cost_start_up, set_hour):

    def obj_expr(m):
        return obj_expr(m, cost_NG, CO2_CREDIT, power_price, cost_start_up, set_hour)
    m.obj = Objective(rule=obj_expr, sense=-1)

    return
