"""
Modeling module
Declare overall variable constraints (as sum of unit variables).

Pengfei Cheng

1. constraints for overall variables (8)
        load factor             fuel rate               CO2 emission rate
        HP steam turbine power  IP steam turbine power  DAC base steam
        allocable steam
"""

from pyomo.environ import *
from ..pyomo_model.params import *


    # 1. CONSTRAINTS FOR OVERALL VARIABLES

    #NOTE: this is tload and not tload_fake
    # load factor
    #def eq_total_load_factor(m, i):
    #    return m.x_load[i] == sum(m.x_load_D[i, mode] for mode in set_mode)
    #m.eq_total_load_factor = Constraint(set_hour_0, rule=eq_total_load_factor)

    #NOTE: the rest of the are alredy dealt with in disaggregated vars
    # fuel consumption
    #def eq_total_fuel_rate(m, i):
    #    return m.x_fuel[i] == sum(m.x_fuel_D[i, mode] for mode in set_mode)
    #m.eq_total_fuel_rate = Constraint(set_hour_0, rule=eq_total_fuel_rate)

    # CO2 emission rate
    #def eq_total_CO2_emission_rate(m, i):
    #    return m.x_CO2_flue[i] == sum(m.x_CO2_D_flue[i, mode] for mode in set_mode)
    #m.eq_total_CO2_emission_rate = Constraint(set_hour_0, rule=eq_total_CO2_emission_rate)

    # HP steam turbine power
    #def eq_total_power_HP(m, i):
    #    return m.x_power_HP[i] == sum(m.x_power_D_HP[i, mode] for mode in set_mode)
    #m.eq_total_power_HP = Constraint(set_hour_0, rule=eq_total_power_HP)

    # IP steam turbine power
    #def eq_total_power_IP(m, i):
    #    return m.x_power_IP[i] == sum(m.x_power_D_IP[i, mode] for mode in set_mode)
    #m.eq_total_power_IP = Constraint(set_hour_0, rule=eq_total_power_IP)

    # DAC base steam
    #def eq_total_DAC_base_duty(m, i):
    #    return m.x_steam_DAC_base[i] == sum(m.x_steam_D_DAC_base[i, mode] for mode in set_mode)
    #m.eq_total_DAC_base_duty = Constraint(set_hour_0, rule=eq_total_DAC_base_duty)

    # allocable steam
    #def eq_total_steam_allocable(m, i):
    #    return m.x_steam_allocable[i] == sum(m.x_steam_D_allocable[i, mode] for mode in set_mode)
    #m.eq_total_steam_allocable = Constraint(set_hour_0, rule=eq_total_steam_allocable)

    # auxiliary power
    #def eq_total_power_aux(m, i):
    #    return m.x_power_aux[i] == sum(m.x_power_D_aux[i, mode] for mode in set_mode)
    #m.eq_total_power_aux = Constraint(set_hour_0, rule=eq_total_power_aux)
