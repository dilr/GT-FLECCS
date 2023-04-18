import pyomo.environ as pe
from ..shared_model import *
from ..shared_model.OM_costing import cost_DAC_FOM
from ..pyomo_model.params import *

cycle_time = 0.75

def create(times, decisions, cost_ng, co2_credit, power_price):
    m = pe.ConcreteModel()

    add_sets(m, times, decisions)
    add_vars(m)
    add_constraints(m)
    add_objective(m, cost_ng, co2_credit, power_price)
    return m

def add_vars(m):
    m.air_adsorb_max = pe.Var(bounds=(0, None))
    m.sorbent_total  = pe.Var(bounds=(0, None))

    m.dsorbent_A       = pe.Var(m.dac_decisions, bounds=(0, None))
    m.tsteam_DAC_extra = pe.Var(m.steam_times,  bounds=(0, None))
    m.tload            = pe.Var(m.steam_times,  bounds=(50, 100))

def add_sets(m, times, decisions):
    m.steam_times = pe.Set(initialize=times)
    m.dac_decisions = pe.Set(initialize=decisions)

def add_constraints(m):
    def air_lt_max(m, d):
        return m.air_adsorb_max >= dair_adsorb(m.dsorbent_A[d])
    m.air_lt_max = pe.Constraint(m.dac_decisions, rule=air_lt_max)
    def dont_overuse_steam(m, d, o):
        #TODO: make generic over cycletime
        #t = int(d//4)+o
        #return frac_time_in_dac(t,d) * tsteam_DAC_total(m.tload[t], m.tsteam_DAC_extra[t], 1) >= dsteam_DAC(m.dsorbent_A[d])
        #GETS THE ADSORPTION PHASE
        t = int((d+2)/4)
        return 0.25*tsteam_DAC_total(m.tload[t], m.tsteam_DAC_extra[t], 1) >= dsteam_DAC(m.dsorbent_A[d])
    m.dont_overuse_steam = pe.Constraint(m.dac_decisions, [0,1], rule=dont_overuse_steam)

    def dont_overcommit_dac(m, d1):
        #TODO: make generic over cycletime
        other_dacs = range(max(d1-2,0), min(d1+3, nhours))
        return sum(m.dsorbent_A[d] for d in other_dacs) <= m.sorbent_total
    m.dont_overcommit_dac = pe.Constraint(m.dac_decisions, rule=dont_overcommit_dac)

def add_objective(m, cost_NG, CO2_CREDIT, power_price):
    def obj(m):
        return obj_expr(m, cost_NG, CO2_CREDIT, power_price)
    m.obj = pe.Objective(rule=obj, sense=-1)

nhours = 12 * 24 * 30 +1
def obj_expr(m, cost_NG, CO2_CREDIT, power_price):
    def fuel_cost(m, t):
        return cost_NG * (a_fuel * m.tload[t] + b_fuel)
    m.fuel_cost = pe.Expression(m.steam_times, rule=fuel_cost)
    
    def tco2_cap(m, t):
        return CO2_CREDIT * tCO2_cap_total(m.tload[t])
    m.tco2_cap = pe.Expression(m.steam_times, rule=tco2_cap)

    def tco2_compr(m, t):
        return a_cost_CO2_TS * tCO2_compress(m.tload[t])
    m.tco2_compr = pe.Expression(m.steam_times, rule=tco2_compr)

    def tpower_cost(m, t):
        return power_price[t] * tpower_net(m.tload[t], m.tload[t], m.tsteam_DAC_extra[t], 1, 1)
    m.tpower_cost = pe.Expression(m.steam_times, rule=tpower_cost)

    def tvom_cost(m, t):
        return tcost_NGCC_VOM(m.tload[t]) + tcost_PCC_VOM(m.tload[t]) + tcost_PCC_compr_VOM(m.tload[t])
    m.tvom_cost = pe.Expression(m.steam_times, rule=tvom_cost)

    def dco2_cap(m, d):
        return CO2_CREDIT * dCO2_cap_total(m.dsorbent_A[d])
    m.dco2_cap = pe.Expression(m.dac_decisions, rule=dco2_cap)

    def dco2_compr(m, d):
        return a_cost_CO2_TS * dCO2_compress(m.dsorbent_A[d])
    m.dco2_compr = pe.Expression(m.dac_decisions, rule=dco2_compr)

    def ddac_power(m, d):
        #return (power_price[int(d//4)]+(power_price[int((d+1)//4)] if int((d+1)//4) < nhours else 0))/2 * dpower_DAC(m.dsorbent_A[d]) 
        return (power_price[int(d//4)]+power_price[int((d+1)//4)])/2 * dpower_DAC(m.dsorbent_A[d]) 
    m.ddac_power = pe.Expression(m.dac_decisions, rule=ddac_power)

    def dcompr_power(m, d):
        #return (power_price[int((d+2)//4)]/4 if int((d+2)//4) < nhours else 0) * dpower_compress(m.dsorbent_A[d]) 
        return power_price[int((d+2)//4)] * dpower_compress(m.dsorbent_A[d]) 
    m.dcompr_power = pe.Expression(m.dac_decisions, rule=dcompr_power)

    def dvom_cost(m, d):
        return dcost_DAC_VOM(m.dsorbent_A[d]) + dcost_DAC_compr_VOM(m.dsorbent_A[d])
    m.dvom_cost = pe.Expression(m.dac_decisions, rule=dvom_cost)
    return \
        ( sum(
             - m.fuel_cost[t] + \
                m.tco2_cap[t] - \
                m.tco2_compr[t] + \
                m.tpower_cost[t] - \
                m.tvom_cost[t]
            for t in m.steam_times) \
        +sum(
                m.dco2_cap[d] - \
                m.dco2_compr[d] - \
                m.ddac_power[d] - \
                m.dcompr_power[d] - \
                m.dvom_cost[d]
            for d in m.dac_decisions)
        - cost_DAC_FOM(m.air_adsorb_max, m.sorbent_total) ) * (1 - tax_r) * sum(1 / (1 + int_r) ** j for j in range(2, 21 + 1)) \
        - cost_DAC_TPC(m.air_adsorb_max, m.sorbent_total) * (1 + 0.0311 + 0.0066 + 0.1779) * ( 0.3 + 0.7 / (1 + int_r) - sum(tax_r * depreciate_r * ((1 - depreciate_r) ** j) * ((1 + int_r) ** (- j - 2)) for j in range(19 + 1)) )

