import pyomo.environ as pe
from .lp import create
from ..pyomo_model.params import *
from ..shared_model import *
from pathlib import Path
import pandas as pd

nhours = 12 * 24 * 30+1
hours = range(nhours)
decisions = range(4*nhours-2)

CO2_CREDIT = 300
cost_NG = 3.83
script_path = Path(__file__, '../..').resolve()
df_power_price = pd.read_csv(str(script_path.joinpath('resources/overall-price-signals.csv')))
df_power_price = df_power_price.dropna()
power_price = df_power_price.loc[:,'MiNg_150_NYISO']

input_dir = '../compr/results/NG-383-300-MiNg_150_NYISO/'

m = create(hours, decisions, cost_NG, CO2_CREDIT, power_price)

op_cost = pd.read_csv(input_dir + 'results_operation_cost.csv')
co2_results = pd.read_csv(input_dir + 'results_CO2.csv')
power_vars = pd.read_csv(input_dir + 'results_power.csv')
load = power_vars['x_load']
m.tload.set_values(load)

dac_costs = pd.read_csv(input_dir + 'results_DAC_costing.csv')
sorbent_total = dac_costs['x_sorbent_total']
m.sorbent_total.value = sorbent_total[0]
air_adsorb_max = dac_costs['x_air_adsorb_max']
m.air_adsorb_max.value = air_adsorb_max[0]

steam_vars = pd.read_csv(input_dir + 'results_steam.csv')
steam_DAC_extra = steam_vars['x_steam_DAC_extra']
m.tsteam_DAC_extra.set_values(steam_DAC_extra)

dac_vars = pd.read_csv(input_dir + 'results_DAC_air.csv')
sorbent_A0 = dac_vars['x_sorbent_A0']
m.dsorbent_A.set_values(sorbent_A0[:-2])

print(f'Objective value: {pe.value(m.obj)}')
print(f'fuel: {sum(pe.value(m.fuel_cost[t]) for t in m.steam_times)} vs {sum(op_cost["cost_fuel"])}')
print(f'co2_cap: {sum(pe.value(m.tco2_cap[t]) for t in m.steam_times) + sum(pe.value(m.dco2_cap[d]) for d in m.dac_decisions)} vs {CO2_CREDIT * sum(co2_results["x_CO2_cap_total"])}')
breakpoint()
#m.pprint()
