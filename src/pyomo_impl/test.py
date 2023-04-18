import pyomo.environ as pe
import pandas as pd
import numpy as np
from pathlib import Path
from .lp import create
from ..pyomo_model.params import *
from ..shared_model import *

nhours = 12 * 24 * 30+1
hours = range(nhours)
decisions = range(4*nhours)

CO2_CREDIT = 300
cost_NG = 3.83

script_path = Path(__file__, '../..').resolve()
df_power_price = pd.read_csv(str(script_path.joinpath('resources/overall-price-signals.csv')))
df_power_price = df_power_price.dropna()
power_price = df_power_price.loc[:,'MiNg_150_NYISO'].to_numpy()[:nhours]
power_price_padded = np.pad(power_price,(0,4))

#m = create(hours, decisions, cost_NG, 300, power_price)

input_dir = '../compr/results/NG-383-300-MiNg_150_NYISO/'

power_vars = pd.read_csv(input_dir + 'results_power.csv')
load = power_vars['x_load']
#m.tload.set_values(load)
load = load.to_numpy()

dac_costs = pd.read_csv(input_dir + 'results_DAC_costing.csv')
sorbent_total = dac_costs['x_sorbent_total']
#m.sorbent_total.value = sorbent_total[0]
air_adsorb_max = dac_costs['x_air_adsorb_max']
#m.air_adsorb_max.value = air_adsorb_max[0]

steam_vars = pd.read_csv(input_dir + 'results_steam.csv')
steam_DAC_extra = steam_vars['x_steam_DAC_extra']
#m.tsteam_DAC_extra.set_values(steam_DAC_extra)
steam_DAC_extra = steam_DAC_extra.to_numpy()

dac_vars = pd.read_csv(input_dir + 'results_DAC_air.csv')
sorbent_A0 = dac_vars['x_sorbent_A0'].to_numpy()
#m.dsorbent_A.set_values(sorbent_A0)

def talif(df, shift=0):
    #return df.groupby((df.index+shift)//4).sum()
    if shift > 0:
        df = np.roll(df, shift)
        df[-shift:] = 0
    elif shift < 0:
        df = np.roll(df, shift)
        df[:-shift] = 0
    df.shape=(-1,4)
    return np.add.reduce(df, axis=1)

def h0_to_h(s):
    #return s.iloc[1:].set_axis(range(s.size-1), copy=False)
    return s

def metho(a):
    gem = np.add.reduce(np.reshape(a,(-1,4)), axis=1)
    mi = a[3::4] /2
    gem -= mi
    gem += np.roll(mi,1)
    gem[-1] -= mi[0]
    return gem

overall_profit_cost = pd.read_csv(input_dir + 'overall_profit_cost.csv')
cost_DAC_TPC = dac_costs['x_cost_DAC_TPC'].to_numpy()
cost_DAC_FOM = cost_DAC_TPC*0.05+110000
op_cost = pd.read_csv(input_dir + 'results_operation_cost.csv')
co2_results = pd.read_csv(input_dir + 'results_CO2.csv')
power_results = pd.read_csv(input_dir + 'results_power.csv')
fuel = h0_to_h(cost_NG * (a_fuel * load + b_fuel))
co2_cap_total = tCO2_cap_total(load) + talif(dCO2_cap_total(sorbent_A0), 2)
co2_compress = a_cost_CO2_TS * (h0_to_h(tCO2_compress(load)) + talif(dCO2_compress(sorbent_A0), 2))
co2_PCC = tCO2_PCC(load)
co2_DAC = talif(dCO2_DAC(sorbent_A0), 2)
power1 = power_price * (tpower_total(load,load,steam_DAC_extra,1,1) - tpower_PCC(load) - tpower_aux(load, 1))
power1_ans = power_price*(power_results['x_power_total'] - power_results['x_power_PCC'] - power_results['x_power_aux'])
power2 = power_price * metho(dpower_DAC(sorbent_A0))
power2_ans = power_price * power_results['x_power_DAC'].to_numpy()
power3 = power_price * (tpower_net(load, load, steam_DAC_extra,1,1) - metho(dpower_DAC(sorbent_A0)) - talif(dpower_compress(sorbent_A0),2))
power3_ans = power_price * power_results['x_power_net']
#print(f'power net = {np.add.reduce(power3) - np.add.reduce(power3_ans)}')
power4 = power_price * talif(dpower_compress(sorbent_A0),2)
power4_ans = power_price * a_power_compr_DAC * co2_results['x_CO2_DAC']
cost_NGCC_VOM = h0_to_h(tcost_NGCC_VOM(load))
cost_PCC_VOM = h0_to_h(tcost_PCC_VOM(load))
cost_PCC_compr_VOM = h0_to_h(tcost_PCC_compr_VOM(load))
cost_DAC_VOM = talif(dcost_DAC_VOM(sorbent_A0), 2)
cost_DAC_compr_VOM = talif(dcost_DAC_compr_VOM(sorbent_A0), 2)
final = (-fuel + CO2_CREDIT * co2_cap_total - co2_compress + power3 - cost_NGCC_VOM - cost_PCC_VOM - cost_PCC_compr_VOM - cost_DAC_VOM - cost_DAC_compr_VOM - cost_DAC_FOM) * (1 - tax_r) * sum(1 / (1 + int_r) ** j for j in range(2, 21 + 1)) - cost_DAC_TPC * (1 + 0.0311 + 0.0066 + 0.1779) * ( 0.3 + 0.7 / (1 + int_r) - sum(tax_r * depreciate_r * ((1 - depreciate_r) ** j) * ((1 + int_r) ** (- j - 2)) for j in range(19 + 1)) )
print(f'final = {final}')

def compr(name, new, orig):
    diff = new - orig
    mask = abs(diff) > 0.1
    #print(f'{name} diff = {diff.sum()}')
    if mask.any():
        out = pd.DataFrame({'new':new[mask], 'original':orig[mask]})
        print(f'{name}:\n {out}')

#compr("CO2 total output", co2_cap_total, co2_results['x_CO2_cap_total'])
compr("fuel cost", fuel, op_cost['cost_fuel'])
compr("CO2 cap total", co2_cap_total, co2_results['x_CO2_cap_total'])
compr("CO2 compress", co2_compress, op_cost['cost_CO2_TS'])
compr("CO2 PCC", co2_PCC, co2_results['x_CO2_PCC'])
compr("CO2 DAC", co2_DAC, co2_results['x_CO2_DAC'])
compr("time power", power1, power1_ans)
compr("DAC power", power2, power2_ans)
compr("total power", power3, power3_ans)
compr("Dac compr power", power4, power4_ans)
compr("NGCC cost", cost_NGCC_VOM, op_cost['cost_NGCC_VOM'])
compr("PCC cost", cost_PCC_VOM, op_cost['cost_PCC_VOM'])
compr("PCC compression cost", cost_PCC_compr_VOM, op_cost['cost_PCC_compr_VOM'])
compr("DAC cost", cost_DAC_VOM, op_cost['cost_DAC_VOM'])
compr("DAC compression cost", cost_DAC_compr_VOM, op_cost['cost_DAC_compr_VOM'])
#s = pe.SolverFactory('gurobi')
#r = s.solve(m, tee=True)

#print(f'Objective value: {pe.value(m.obj)}')
#m.pprint()
