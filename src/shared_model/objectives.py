from ..pyomo_model.params import a_cost_CO2_TS, a_fuel, b_fuel
from .OM_costing import cost_DAC_FOM, tcost_NGCC_VOM, tcost_PCC_VOM, tcost_PCC_compr_VOM, dcost_DAC_VOM, dcost_DAC_compr_VOM
from .compress_vent_constraints import tCO2_cap_total, tCO2_compress, dCO2_cap_total, dCO2_compress, dpower_compress
from .power_constraints import tpower_net, tpower_GT
from .DAC_constraints import dpower_DAC

def tfuel_cost(tload, cost_NG):
    return cost_NG * (a_fuel * tload + b_fuel)

def tco2_cap(tload, CO2_CREDIT):
    return CO2_CREDIT * tCO2_cap_total(tload)

def tco2_compr(tload):
    return a_cost_CO2_TS * tCO2_compress(tload)

def tpower_cost(tload, tsteam_DAC_extra, power_price):
    return power_price * (tpower_net(tload, tsteam_DAC_extra, 1) + tpower_GT(tload, 1))

def tvom_cost(tload):
    return tcost_NGCC_VOM(tload) + tcost_PCC_VOM(tload) + tcost_PCC_compr_VOM(tload)

def dco2_cap(dsorbent_A, CO2_CREDIT):
    return CO2_CREDIT * dCO2_cap_total(dsorbent_A)

def dco2_compr(dsorbent_A):
    return a_cost_CO2_TS * dCO2_compress(dsorbent_A)

#TODO: unify implementations.
def ddac_power(dsorbent_A, power_price):
    #return (power_price[int(d//4)]+power_price[int((d+1)//4)])/2 * dpower_DAC(m.dsorbent_A[d]) 
    return power_price * dpower_DAC(dsorbent_A) 

def dcompr_power(dsorbent_A, power_price):
    #return (power_price[int((d+2)//4)]/4 if int((d+2)//4) < nhours else 0) * dpower_compress(m.dsorbent_A[d]) 
    return power_price * dpower_compress(dsorbent_A) 

def dvom_cost(dsorbent_A):
    return dcost_DAC_VOM(dsorbent_A) + dcost_DAC_compr_VOM(dsorbent_A)

def obj(tload, tsteam_DAC_extra, dsorbent_A, cost_NG, CO2_CREDIT, power_price):
    return - tfuel_cost(tload, cost_NG) + tco2_cap(tload, CO2_CREDIT) - tco2_compr(tload) + tpower_cost(tload, tsteam_DAC_extra, power_price) - tvom_cost(tload) + dco2_cap(dsorbent_A, CO2_CREDIT) - dco2_compr(dsorbent_A) - ddac_power(dsorbent_A, power_price) - dcompr_power(dsorbent_A, power_price) - dvom_cost(dsorbent_A)
