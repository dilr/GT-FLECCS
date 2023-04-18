"""
Modeling module
Declare disaggregated variable constraints.

Pengfei Cheng

1.  convex combination of lam = x_load_D (at dispatch mode)
2.  load factor during start-up
3.  load big-M

4.  fuel rate at dispatch mode
5.  fuel rate at start-up

6.  CO2 emission rate at dispatch mode
7.  CO2 emission rate at start-up

8.  constraints for other disaggregated variables at each mode (8)
        HP steam turbine power  IP steam turbine power
        DAC base steam          allocable steam
"""

from pyomo.environ import *
from ..pyomo_model.params import *

    # 1. CONVEX COMBINATION OF lam = X_LOAD_FACTOR_D (AT DISPATCH MODE)
    #    load factor is a convex combination of extreme points
    #def eq_lam_load(m, i):
    #    return sum(m.lam[i, k] * x_range[k] for k in x_range_extreme_points) == m.x_load_D[i, dispatch_idx]
    #import logging
    #m.eq_lam_load = Constraint(set_hour_0, rule=eq_lam_load)
def tload_D_disp(tlam1, tlam2):
    return x_range[1] * tlam1 + x_ramge2 * tlam2

    # --------------------------------------------------------------------------

    # 2. LOAD DURING START-UP
    #def eq_load_start_up(m, i):
    #    return m.x_load_D[i, start_up_idx] == sum((m.z0[i - k + 1]) * load_trajectory[k] for k in set_start_up_hour if i - k + 1>= 0)
    #m.eq_load_start_up = Constraint(set_hour_0, rule=eq_load_start_up)
def tload_D_startup(z0):
    return sum((z0[i-k+1]) * load_trajectory[k] for k in set_start_up_hour if i - k + 1>=0)

    # --------------------------------------------------------------------------

    #TODO: make into constraint
    # 3. LOAD BIG-M
    # for both modes, x_load_D = 0 when y = 0
    #def eq_off_mode_load(m, i, j):
    #    return m.x_load_D[i, j] <= 100 * m.y[i]
    #m.eq_off_mode_load = Constraint(set_hour_0, set_mode, rule=eq_off_mode_load)

    # --------------------------------------------------------------------------

    # 4. FUEL RATE AT DISPATCH MODE
    #def eq_fuel_dispatch(m, i):
    #    return m.x_fuel_D[i, dispatch_idx] == a_fuel * m.x_load_D[i, dispatch_idx] + b_fuel * (m.y[i] - m.z[i])
    #m.eq_fuel_dispatch = Constraint(set_hour_0, rule=eq_fuel_dispatch)
    #NOTE: separate dispatch from startup later
    #NOTE: dispatched is y - z
def tfuel_D(tlam1, tlam2, dispatched):
    return a_fuel * t_load_D_dispatch(tlam1, tlam2) + b_fuel * dispatched

    # --------------------------------------------------------------------------

    #NOTE: separate dispatch from startup later
    # 5. FUEL RATE AT START-UP
    #def eq_fuel_start_up(m, i):
    #    return m.x_fuel_D[i, start_up_idx] == 0
    #m.eq_fuel_start_up = Constraint(set_hour_0, rule=eq_fuel_start_up)

    # --------------------------------------------------------------------------

    # 6. CO2 EMISSION RATE AT DISPATCH MODE
    #def eq_emission_dispatch(m, i):
    #    return m.x_CO2_D_flue[i, dispatch_idx] == a_CO2_flue * m.x_load_D[i, dispatch_idx] + b_CO2_flue * (m.y[i] - m.z[i])
    #m.eq_emission_dispatch = Constraint(set_hour_0, rule=eq_emission_dispatch)
    #NOTE: separate dispatch from startup later
def tCO2_flue(tfake_load, dispatched):
    return a_CO2_flue * tfake_load + b_CO2_flue * dispatched

    # --------------------------------------------------------------------------

    #NOTE: separate dispatch from startup later
    # 7. CO2 EMISSION RATE AT START-UP
    #def eq_emission_start_up(m, i):
    #    return m.x_CO2_D_flue[i, start_up_idx] == 0
    #m.eq_emission_start_up = Constraint(set_hour_0, rule=eq_emission_start_up)

    # --------------------------------------------------------------------------

    # 13. CONSTRAINTS FOR OTHER DISJUNCTIVE VARIABLES AT EACH MODE

    # HP steam turbine power
    #def eq_power_HP_dispatch(m, i):
    #    return m.x_power_D_HP[i, dispatch_idx] == a_power_HP * m.x_load_D[i, dispatch_idx] + b_power_HP * (m.y[i] - m.z[i])
    #m.eq_power_HP_dispatch = Constraint(set_hour_0, rule=eq_power_HP_dispatch)
    #NOTE: separate dispatch from startup later
def tpower_HP(tfake_load, dispatched):
    return a_power_HP * tfake_load + b_power_HP * dispatched

    #def eq_power_HP_start_up(m, i):
    #    return m.x_power_D_HP[i, start_up_idx] == 0
    #m.eq_power_HP_start_up = Constraint(set_hour_0, rule=eq_power_HP_start_up)

    # IP steam turbine power
    #def eq_power_IP_dispatch(m, i):
    #    return m.x_power_D_IP[i,dispatch_idx] == a_power_IP * m.x_load_D[i,dispatch_idx] + b_power_IP * (m.y[i]-m.z[i])
    #m.eq_power_IP_dispatch = Constraint(set_hour_0, rule=eq_power_IP_dispatch)
    #def eq_power_IP_start_up(m, i):
    #    return m.x_power_D_IP[i,start_up_idx] == 0
    #m.eq_power_IP_start_up = Constraint(set_hour_0, rule=eq_power_IP_start_up)
def tpower_IP(tfake_load, dispatched):
    return a_power_IP * tfake_load + b_power_IP * dispatched


    # DAC base steam
    #def eq_DAC_base_steam_dispatch(m, i):
    #    return m.x_steam_D_DAC_base[i,dispatch_idx] == a_steam_DAC_base * m.x_load_D[i,dispatch_idx] + b_steam_DAC_base * (m.y[i] - m.z[i])
    #m.eq_DAC_base_steam_dispatch = Constraint(set_hour_0, rule=eq_DAC_base_steam_dispatch)
    #def eq_DAC_base_steam_start_up(m, i):
    #    return m.x_steam_D_DAC_base[i,start_up_idx] == 0
    #m.eq_DAC_base_steam_start_up = Constraint(set_hour_0, rule=eq_DAC_base_steam_start_up)
def tsteam_DAC_base(tfake_load, dispatched):
    return a_steam_DAC_base * tfake_load + b_steam_DAC_base * dispatched


    # allocable steam
    #def eq_allocable_steam_dispatch(m, i):
    #    return m.x_steam_D_allocable[i,dispatch_idx] == a_steam_alloc * m.x_load_D[i,dispatch_idx] + b_steam_alloc * (m.y[i] - m.z[i])
    #m.eq_allocable_steam_dispatch = Constraint(set_hour_0, rule=eq_allocable_steam_dispatch)
    #def eq_allocable_steam_start_up(m, i):
    #    return m.x_steam_D_allocable[i,start_up_idx] == 0
    #m.eq_allocable_steam_start_up = Constraint(set_hour_0, rule=eq_allocable_steam_start_up)
def tsteam_allocable(tfake_load, dispatched):
    return a_steam_alloc * tfake_load + b_steam_alloc * dispatched


    # auxiliary power
    #def eq_auxiliary_power_dispatch(m, i):
    #    return m.x_power_D_aux[i,dispatch_idx] == a_power_aux * m.x_load_D[i,dispatch_idx] + b_power_aux * (m.y[i] - m.z[i])
    #m.eq_auxiliary_power_dispatch = Constraint(set_hour_0, rule=eq_auxiliary_power_dispatch)
    #def eq_auxiliary_power_start_up(m, i):
    #    return m.x_power_D_aux[i,start_up_idx] == 0
    #m.eq_auxiliary_power_start_up = Constraint(set_hour_0, rule=eq_auxiliary_power_start_up)
def tpower_aux(tfake_load, dispatched):
    return a_power_aux * tfake_load + b_power_aux * dispatched

