import math
import pyomo.environ as pe
from ..shared_model import *
from ..shared_model.OM_costing import cost_DAC_FOM
from ..pyomo_model.params import *

cycle_time = 0.75

def create_orig(times, decisions, cost_ng, co2_credit, power_price):
    m = pe.ConcreteModel()

    add_sets(m, times, decisions)
    add_vars(m)
    add_constraints(m)
    add_exprs(m, cost_ng, co2_credit, power_price)
    add_objective_orig(m, cost_ng, co2_credit, power_price)
    return m

def create_test1(times, decisions, cost_ng, co2_credit, power_price):
    m = pe.ConcreteModel()

    add_sets(m, times, decisions)
    add_vars(m)
    m.air_adsorb_max.fix(47795)
    m.sorbent_total.fix(2990)
    add_tank_constraints(m)
    add_exprs(m, cost_ng, co2_credit, power_price)
    add_objective_test1(m, cost_ng, co2_credit, power_price)
    return m

def add_vars(m):
    m.air_adsorb_max = pe.Var(bounds=(0, None))
    m.sorbent_total  = pe.Var(bounds=(0, None))

    m.dsorbent_A       = pe.Var(m.dac_decisions, bounds=(0, None))
    m.tsteam_DAC_extra = pe.Var(m.steam_times,  bounds=(0, None))
    m.tload            = pe.Var(m.steam_times,  bounds=(50, 100))

# decicion# * cycle_time = time cycle starts
# so if we want all decision # within an hour, note that
# time / cycletime ≤ decision# < (time+1)/cycletime
# decisions availible is all ints which fit this
# |decisions| = ceil((t+1)/cycle_time - ceil(t/cycle_time)) - 1
def t_to_d_map(t):
    d = int(math.ceil(t/cycle_time))
    d_end = (t+1)/cycle_time
    while d < d_end:
        yield d
        d += 1
    return

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

def add_tank_constraints(m):
    def air_lt_max(m, d):
        return m.air_adsorb_max >= dair_adsorb(m.dsorbent_A[d])/15/60
    m.air_lt_max = pe.Constraint(m.dac_decisions, rule=air_lt_max)

    def dont_overuse_steam(m, t):
        return tsteam_DAC_total(m.tload[t], m.tsteam_DAC_extra[t], 1) >= pe.quicksum(
            dsteam_DAC(m.dsorbent_A[d]) for d in t_to_d_map(t)
        )
    m.dont_overuse_steam = pe.Constraint(m.steam_times, rule=dont_overuse_steam)

    def dont_overcommit_steam(m, t):
        return tsteam_allocable(m.tload[t], 1) >= m.tsteam_DAC_extra[t]
    m.dont_overcommit_steam = pe.Constraint(m.steam_times, rule=dont_overcommit_steam)

    def dont_overcommit_dac(m, d):
        return m.dsorbent_A[d] <= m.sorbent_total
    m.dont_overcommit_dac = pe.Constraint(m.dac_decisions, rule=dont_overcommit_dac)

def add_exprs(m, cost_NG, CO2_CREDIT, power_price):
    def fuel_cost_rule(m, t):
        return tfuel_cost(m.tload[t], cost_NG)
    m.fuel_cost = pe.Expression(m.steam_times, rule=fuel_cost_rule)
    
    def tco2_cap_rule(m, t):
        return tco2_cap(m.tload[t], CO2_CREDIT)
    m.tco2_cap = pe.Expression(m.steam_times, rule=tco2_cap_rule)

    def tco2_compr_rule(m, t):
        return tco2_compr(m.tload[t])
    m.tco2_compr = pe.Expression(m.steam_times, rule=tco2_compr_rule)

    def tpower_cost_rule(m, t):
        return tpower_cost(m.tload[t], m.tsteam_DAC_extra[t], power_price[t])
    m.tpower_cost = pe.Expression(m.steam_times, rule=tpower_cost_rule)

    def tvom_cost_rule(m, t):
        return tvom_cost(m.tload[t])
    m.tvom_cost = pe.Expression(m.steam_times, rule=tvom_cost_rule)

    def dco2_cap_rule(m, d):
        return dco2_cap(m.dsorbent_A[d], CO2_CREDIT)
    m.dco2_cap = pe.Expression(m.dac_decisions, rule=dco2_cap_rule)

    def dco2_compr_rule(m, d):
        return dco2_compr(m.dsorbent_A[d])
    m.dco2_compr = pe.Expression(m.dac_decisions, rule=dco2_compr_rule)

    def ddac_power_rule(m, d):
        return ddac_power(m.dsorbent_A[d], power_price[math.floor(d*cycle_time)]) 
    m.ddac_power = pe.Expression(m.dac_decisions, rule=ddac_power_rule)

    def dcompr_power_rule(m, d):
        return dcompr_power(m.dsorbent_A[d], power_price[math.floor(d*cycle_time)])
    m.dcompr_power = pe.Expression(m.dac_decisions, rule=dcompr_power_rule)

    def dvom_cost_rule(m, d):
        return dvom_cost(m.dsorbent_A[d]) 
    m.dvom_cost = pe.Expression(m.dac_decisions, rule=dvom_cost_rule)

def add_objective_test1(m, cost_NG, CO2_CREDIT, power_price):
    def obj_expr(m,t):
        return - m.fuel_cost[t] + \
                m.tco2_cap[t] - \
                m.tco2_compr[t] + \
                m.tpower_cost[t] - \
                m.tvom_cost[t] + \
                pe.quicksum(
                    m.dco2_cap[d] - \
                    m.dco2_compr[d] - \
                    m.ddac_power[d] - \
                    m.dcompr_power[d] - \
                    m.dvom_cost[d]
                for d in t_to_d_map(t))
    m.obj_expr = pe.Expression(m.steam_times, rule=obj_expr)
    m.obj = pe.Objective(sense=-1, expr=pe.quicksum(m.obj_expr.values()))

nhours = 12 * 24 * 30 +1
def add_objective_orig(m, cost_NG, CO2_CREDIT, power_price):

    m.obj = pe.Objective(sense=-1, expr=
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
        )) #- cost_DAC_FOM(m.air_adsorb_max, m.sorbent_total) ) * (1 - tax_r) * sum(1 / (1 + int_r) ** j for j in range(2, 21 + 1)) \
        #- cost_DAC_TPC(m.air_adsorb_max, m.sorbent_total) * (1 + 0.0311 + 0.0066 + 0.1779) * ( 0.3 + 0.7 / (1 + int_r) - sum(tax_r * depreciate_r * ((1 - depreciate_r) ** j) * ((1 + int_r) ** (- j - 2)) for j in range(19 + 1)) ))

