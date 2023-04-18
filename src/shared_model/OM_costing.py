"""
Modeling module
Constraints related to costing.

Pengfei Cheng
2023
"""

from pyomo.environ import *
from ..pyomo_model.params import *
from .DAC_constraints import dCO2_DAC
from .DAC_costing_constraints import cost_DAC_TPC



    # FOM of DAC
    #def eq_FOM_DAC(m):
    #    return m.x_cost_DAC_FOM == m.x_cost_DAC_TPC*0.05+2*110000
    #m.eq_FOM_DAC = Constraint(rule=eq_FOM_DAC)
def cost_DAC_FOM(air_adsorb_max, sorbent_total):
    return cost_DAC_TPC(air_adsorb_max, sorbent_total)*0.05+2*110000

    # VOM of NGCC
    #def eq_VOM_NGCC(m, i):
    #    return m.x_cost_NGCC_VOM[i] == a_cost_NGCC_VOM * m.x_load[i]
    #m.eq_VOM_NGCC = Constraint(set_hour_0, rule=eq_VOM_NGCC)
def tcost_NGCC_VOM(tload):
    return a_cost_NGCC_VOM * tload

    # VOM of PCC
    #def eq_cost_PCC_VOM(m, i):
    #    return m.x_cost_PCC_VOM[i] == a_cost_PCC_VOM * m.x_load[i]
    #m.eq_cost_PCC_VOM = Constraint(set_hour_0, rule=eq_cost_PCC_VOM)
def tcost_PCC_VOM(tload):
    return a_cost_PCC_VOM * tload

    # VOM of DAC
    #def eq_cost_DAC_VOM(m, i):
    #    return m.x_cost_DAC_VOM[i] == a_cost_DAC_VOM * sum(m.x_CO2_DAC[i,j] for j in set_quarter)
    #m.eq_cost_DAC_VOM = Constraint(set_hour_0, rule=eq_cost_DAC_VOM)
def dcost_DAC_VOM(dsorbent_A):
    return a_cost_DAC_VOM * dCO2_DAC(dsorbent_A)

    # VOM of PCC compressor
    #def eq_cost_PCC_compr_VOM(m, i):
    #    return m.x_cost_PCC_compr_VOM[i] == a_cost_PCC_compr_VOM * m.x_load[i]
    #m.eq_cost_PCC_compr_VOM = Constraint(set_hour_0, rule=eq_cost_PCC_compr_VOM)
def tcost_PCC_compr_VOM(tload):
    return a_cost_PCC_compr_VOM * tload

    # VOM of DAC compressor
    #def eq_VOM_DAC_compressor(m, i):
    #    return m.x_cost_DAC_compr_VOM[i] == a_cost_DAC_compr_VOM * sum(m.x_CO2_DAC[i, j] for j in set_quarter)
    #m.eq_VOM_DAC_compressor = Constraint(set_hour_0, rule=eq_VOM_DAC_compressor)
def dcost_DAC_compr_VOM(dsorbent_A):
    return a_cost_DAC_compr_VOM * dCO2_DAC(dsorbent_A)

