"""
Modeling module
Declare steam split constraints.

Pengfei Cheng

1. steam allocation
2. total DAC steam
3. DAC steam slack
4. steam rate limit

UPDATE:
    01-21-2022: added steam rate limit constraint.
"""

from pyomo.environ import *
from ..pyomo_model.params import *
from .disaggregated_constraints import tsteam_DAC_base, tsteam_allocable


#def add_steam_split_constraints(m, set_hour_0):

    # 1. STEAM ALLOCATION
    #def eq_steam_allocation(m, i):
    #    return m.x_steam_allocable[i] == m.x_steam_DAC_extra[i] + m.x_steam_LP[i]
    #m.eq_steam_allocation = Constraint(set_hour_0, rule=eq_steam_allocation)
def tsteam_LP(tload, tsteam_DAC_extra, disp):
    return tsteam_allocable(tload, disp) - tsteam_DAC_extra

    # --------------------------------------------------------------------------

    # 2. TOTAL DAC STEAM
    #def eq_DAC_total_duty(m, i):
    #    return m.x_steam_DAC_total[i] == m.x_steam_DAC_base[i] + m.x_steam_DAC_extra[i]
    #m.eq_DAC_total_duty = Constraint(set_hour_0, rule=eq_DAC_total_duty)
def tsteam_DAC_total(tfake_load, tsteam_DAC_extra, disp):
    return tsteam_DAC_base(tfake_load, disp) + tsteam_DAC_extra

    # --------------------------------------------------------------------------

    #TODO: add as constraint to model
    # 3. DAC STEAM SLACK
    # integral over all slices within each hour
    #def eq_DAC_steam_slack_int(m, i):
    #    return m.x_steam_DAC_total[i] >= sum(m.x_steam_DAC[i, j] for j in set_quarter)
    #m.eq_DAC_steam_slack_int = Constraint(set_hour_0, rule=eq_DAC_steam_slack_int)

    # --------------------------------------------------------------------------

    #TODO: add as constraint to model
    # 4. STEAM RATE LIMIT
    # 15-min steam into DACs cannot exceed 1/4 of 1-hour available steam
    #def eq_DAC_steam_rate_limit(m, i, j):
    #    return m.x_steam_DAC_total[i] / 4 >= m.x_steam_DAC[i, j]
    #m.eq_DAC_steam_rate_limit = Constraint(set_hour_0, set_quarter, rule=eq_DAC_steam_rate_limit)

