"""
Modeling module
Declare variables.

Pengfei Cheng

1. overall variables
        combustion turbine          steam turbine               PCC
        DAC                         compression & vented CO2    power

2. operation mode logic variables
        lambda                      y                           z0

3. disaggregated variables
4. DAC operational variables
5. costing variables
"""

from pyomo.environ import *
from .params import *

def declare_variables(m, set_hour_0):

    # 1. OVERALL VARIABLES
    #    indexed by hour
    #    basic variables that describe the operations of each unit.

    # 1.1 COMBUSTION TURBINE
    # overall load factor, from 0 to 100 (as sum of single GT load factor)
    m.x_load = Var(set_hour_0, bounds=(0, 100))
    # overall power produced by GTs
    m.x_power_GT = Var(set_hour_0, bounds=(0, None))
    # natural gas fuel rate
    m.x_fuel = Var(set_hour_0, bounds=(0, None))
    # CO2 emission from burning natural gas
    m.x_CO2_flue = Var(set_hour_0, bounds=(0, None))

    # 1.2 STEAM TURBINE
    # power generation from HP steam
    m.x_power_HP = Var(set_hour_0, bounds=(0, None))
    # power generation from IP steam
    m.x_power_IP = Var(set_hour_0, bounds=(0, None))
    # power generation from LP steam
    m.x_power_LP = Var(set_hour_0, bounds=(0, None))
    # power generated by steam turbine
    m.x_power_ST = Var(set_hour_0, bounds=(0, None))
    # energy allocated for LP power generation
    m.x_steam_LP = Var(set_hour_0, bounds=(0, None))
    # allocatable energy load for LP power/DAC
    m.x_steam_allocable = Var(set_hour_0, bounds=(0, None))

    # 1.3 PCC
    # CO2 captured by PCC
    m.x_CO2_PCC = Var(set_hour_0, bounds=(0, None))
    # steam use of PCC
    m.x_steam_PCC = Var(set_hour_0, bounds=(0, None))
    # power use of PCC
    m.x_power_PCC = Var(set_hour_0, bounds=(0, None))
    # CO2 vented at the outlet of PCC
    m.x_CO2_vent_PCC = Var(set_hour_0, bounds=(0, None))

    # 1.4 DAC
    # base energy for DAC units regeneration
    m.x_steam_DAC_base = Var(set_hour_0, bounds=(0, None))
    # additional energy for the DAC steam generation unit
    m.x_steam_DAC_extra = Var(set_hour_0, bounds=(0, None))
    # overall energy for DAC units regeneration (base + additional)
    m.x_steam_DAC_total = Var(set_hour_0, bounds=(0, None))

    # 1.5 COMPRESSION & VENTED CO2
    m.x_CO2_compress = Var(set_hour_0, bounds=(0, None))
    m.x_power_compress = Var(set_hour_0, bounds=(0, None))
    # total captured CO2 (when positive)/vented CO2 (when negative)
    m.x_CO2_cap_total = Var(set_hour_0)

    # 1.6 POWER
    # total power (sum of GTs and STs)
    m.x_power_total = Var(set_hour_0, bounds=(0, None))
    # net power out
    m.x_power_net = Var(set_hour_0, bounds=(0, None))
    # total auxiliary power
    m.x_power_aux = Var(set_hour_0, bounds=(0, None))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # 2. OPERATION MODEL LOGIC VARIABLES
    #    indexed by hour

    # convex weight of each extreme point (50, 100) for dispatch mode
    # continuous, 0 to 1
    m.lam = Var(set_hour_0, x_range_extreme_points, bounds=(0, 1))

    # if plant is on
    # binary
    m.y = Var(set_hour_0, within=Binary, initialize=1)

    # if plant starts up at hour i
    # binary
    m.z0 = Var(set_hour_0, within=Binary, initialize=0)

    # if plant is during the start-up period
    # binary
    m.z = Var(set_hour_0, within=Binary, initialize=0)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # 3. DISAGGREGATED VARIABLES
    #    indexed by hour and mode (start-up, or normal dispatch)

    m.x_load_D = Var(set_hour_0, set_mode, bounds=(0, None))
    m.x_power_D_HP = Var(set_hour_0, set_mode, bounds=(0, None))
    m.x_power_D_IP = Var(set_hour_0, set_mode, bounds=(0, None))
    m.x_power_D_aux = Var(set_hour_0, set_mode, bounds=(0, None))
    m.x_fuel_D = Var(set_hour_0, set_mode, bounds=(0, None))
    m.x_CO2_D_flue = Var(set_hour_0, set_mode, bounds=(0, None))
    m.x_steam_D_DAC_base = Var(set_hour_0, set_mode, bounds=(0, None))
    m.x_steam_D_allocable = Var(set_hour_0, set_mode, bounds=(0, None))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------


    # 4. DAC OPERATIONAL VARIABLES
    #    indexed by hour, 15-min

    m.x_sorbent_A0 = Var(set_hour_0, set_quarter, bounds=(0, None))
    m.x_sorbent_A1 = Var(set_hour_0, set_quarter_0, bounds=(0, None))
    m.x_sorbent_R = Var(set_hour_0, set_quarter, bounds=(0, None))
    m.x_sorbent_F = Var(set_hour_0, set_quarter_0, bounds=(0, None))
    m.x_sorbent_S = Var(set_hour_0, set_quarter_0, bounds=(0, None))
    m.x_CO2_DAC = Var(set_hour_0, set_quarter, bounds=(0, None))
    m.x_steam_DAC = Var(set_hour_0, set_quarter, bounds=(0, None))
    m.x_power_DAC = Var(set_hour_0, set_quarter, bounds=(0, None))

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    # 5. COSTING VARIABLES
    #    no index

    # amount of total sorbent for air, tonne
    m.x_sorbent_total = Var(bounds=(0, None))
    # fix(x_sorbent_total, 2990, force=true)
    # total cost of sorbent, $
    m.x_cost_sorbent = Var(bounds=(0, None))

    # max adsorption air rate, m^3/s
    m.x_air_adsorb_max = Var(bounds=(0, None))

    # air volume blown for DAC-air adsorption in the next slice (15 min), m^3
    m.x_air_adsorb = Var(set_hour_0, set_quarter_0, bounds=(0, None))

    # adsorption system cost, $
    m.x_cost_adsorb = Var(bounds=(0, None))

    # total capital cost of DACs, $
    # TPC
    m.x_cost_DAC_TPC = Var(bounds=(0, None))

    # DAC FOM, $/yr
    m.x_cost_DAC_FOM = Var(bounds=(0, None))

    # VOMs, $
    m.x_cost_NGCC_VOM = Var(set_hour_0, bounds=(0, None))
    m.x_cost_PCC_VOM = Var(set_hour_0, bounds=(0, None))
    m.x_cost_DAC_VOM = Var(set_hour_0, bounds=(0, None))
    m.x_cost_PCC_compr_VOM = Var(set_hour_0, bounds=(0, None))
    m.x_cost_DAC_compr_VOM = Var(set_hour_0, bounds=(0, None))

    return