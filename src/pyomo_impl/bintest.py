import pyomo.environ as pe
from .lp import create_test1
from .backtrack import backwards_inf
from ..pyomo_model.params import *
from ..shared_model import *
from pathlib import Path
from timeit import timeit
import cProfile as profile
import pstats
import pandas as pd
import numpy as np

nhours = 12 * 24 * 30+1
hours = list(range(nhours))
decisions = hours

CO2_CREDIT = 300
cost_NG = 3.83
script_path = Path(__file__, '../..').resolve()
df_power_price = pd.read_csv(str(script_path.joinpath('resources/overall-price-signals.csv')))
df_power_price = df_power_price.dropna()
power_price = df_power_price.loc[:,'MiNg_150_NYISO']

# load data without restarts
input_dir = '../compr/results/NG-383-300-MiNg_150_NYISO--wbin/'

#m = create_test1(hours, decisions, cost_NG, CO2_CREDIT, power_price)

op_cost = pd.read_csv(input_dir + 'results_operation_cost.csv')
co2_results = pd.read_csv(input_dir + 'results_CO2.csv')
power_vars = pd.read_csv(input_dir + 'results_power.csv')
load = power_vars['x_load']
#m.tload.set_values(load)

dac_costs = pd.read_csv(input_dir + 'results_DAC_costing.csv')
sorbent_total = dac_costs['x_sorbent_total']
#m.sorbent_total.value = sorbent_total[0]
air_adsorb_max = dac_costs['x_air_adsorb_max']
#m.air_adsorb_max.value = air_adsorb_max[0]

steam_vars = pd.read_csv(input_dir + 'results_steam.csv')
steam_DAC_extra = steam_vars['x_steam_DAC_extra']
#m.tsteam_DAC_extra.set_values(steam_DAC_extra)

dac_vars = pd.read_csv(input_dir + 'results_DAC_air.csv')
sorbent_A0 = dac_vars['x_sorbent_A0']
#m.dsorbent_A.set_values(sorbent_A0.iloc[1::4].set_axis(hours))

tload = load.to_numpy()
tsteam_DAC_extra = steam_DAC_extra.to_numpy()
dsorbent_A = sorbent_A0.to_numpy()[1::4]
power_price = power_price.to_numpy()[:nhours]
def get_obj(s):
    return obj(tload[s], tsteam_DAC_extra[s], dsorbent_A[s], cost_NG, CO2_CREDIT, power_price[s])

#test_hours = slice(None)

test_hours=slice(7400,None)
objv = np.sum(get_obj(test_hours))
good_vals = get_obj(test_hours)
good_prices = power_price[test_hours]
runme = backwards_inf(good_prices)
#times = timeit('runme(good_vals)', number=1000, globals=globals())
#print(times)
#profiler = profile.Profile()
#profiler.run('runme(good_vals)')
#stats = pstats.Stats(profiler)
#stats.print_stats('back_inf')
#exit()
#breakpoint()

# load data with restarts
input_dir = '../compr/results/NG-383-300-MiNg_150_NYISO--final/'

op_cost = pd.read_csv(input_dir + 'results_operation_cost.csv')
bin_vars = pd.read_csv(input_dir + 'results_binary_vars.csv')
co2_results = pd.read_csv(input_dir + 'results_CO2.csv')
power_vars = pd.read_csv(input_dir + 'results_power.csv')
load = power_vars['x_load']

dac_costs = pd.read_csv(input_dir + 'results_DAC_costing.csv')
sorbent_total = dac_costs['x_sorbent_total']
air_adsorb_max = dac_costs['x_air_adsorb_max']

steam_vars = pd.read_csv(input_dir + 'results_steam.csv')
steam_DAC_extra = steam_vars['x_steam_DAC_extra']

dac_vars = pd.read_csv(input_dir + 'results_DAC_air.csv')
sorbent_A0 = dac_vars['x_sorbent_A0']

fuel_cost = op_cost['cost_fuel'].to_numpy()
co2_cap = op_cost['credit_CO2'].to_numpy()
co2_compr = op_cost['cost_CO2_TS'].to_numpy()
power_cost = op_cost['profit_power'].to_numpy()
vom_cost = np.sum(op_cost[['cost_NGCC_VOM', 'cost_PCC_VOM',
    'cost_DAC_VOM', 'cost_PCC_compr_VOM', 'cost_DAC_compr_VOM']].to_numpy(), axis=1)
cost_start_up = 100.45 * CO2_CREDIT + 16958.58 * cost_NG
z0 = bin_vars['z0'].to_numpy()
def get_oobj(s):
    return -fuel_cost[s] + co2_cap[s] - co2_compr[s] + power_cost[s] - vom_cost[s] - cost_start_up * z0[s]

print(f'oobj2 = {np.sum(get_oobj(slice(7400,7400+9)))}')
vals = runme(good_vals)
print(f'oobj = {np.sum(get_oobj(test_hours))}')
print(f'mycalc = {vals}')
#s = pe.SolverFactory('gurobi')
#s.solve(m, tee=True)

print(f'Objective value: {objv}')
#print(f'fuel: {sum(pe.value(m.fuel_cost[t]) for t in m.steam_times)} vs {sum(op_cost["cost_fuel"])}')
#print(f'co2_cap: {sum(pe.value(m.tco2_cap[t]) for t in m.steam_times) + sum(pe.value(m.dco2_cap[d]) for d in m.dac_decisions)} vs {CO2_CREDIT * sum(co2_results["x_CO2_cap_total"])}')
#m.pprint()
