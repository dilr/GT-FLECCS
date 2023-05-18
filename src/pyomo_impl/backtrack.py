import numpy as np
from ..shared_model import *
from ..pyomo_model.params import *

nbuf = 10
startup_time = 9 #h

def _backwards_inf_test(model, power_price):
    good_vals = np.Array(model.obj_expr.values(True))
    return backwards_inf(good_vals, power_price)

def backwards_inf(power_price):
    startup_cost = get_startup_vals(power_price)
    nhours = len(power_price)
    buf = np.zeros((nbuf,7,2))
    # No using more than 5 restarts
    buf[:,6,:] = -np.Inf

    curr_running   = buf[0,:-1,0]
    curr_stopped   = buf[0,:-1,1]
    next_running   = buf[1,:-1,0]
    next_stopped   = buf[1,:-1,1]
    future_running = buf[9,1: ,0]

    temp = np.zeros((6,))
    rollbuf = np.zeros((nbuf-1,7,2))
    va = buf[1: ,...]
    vb = buf[:-1,...]
    vc = buf[1  ,...]
    def back_inf(good_vals):
        # No skipping past the end
        buf[2:,:,0]  = -np.Inf
        # End has no intrinsic reward
        buf[1,:-1,:] = 0
        for val, price, startup in zip(
            reversed(good_vals), reversed(power_price), reversed(startup_cost)):
            
            np.add(val, next_running, out=temp)
            np.maximum(temp, next_stopped, out=curr_running)

            np.add(startup, future_running, out=temp)
            np.maximum(next_stopped, temp, out=curr_stopped)

            np.copyto(va, vb)
        return vc
    return back_inf

def get_startup_vals(power_price):
    CO2_CREDIT = 300
    cost_NG = 3.83
    cost_start_up = 100.45 * CO2_CREDIT + 16958.58 * cost_NG
    
    loads = np.array((0, 0.33, 9.37, 9.98, 14.27, 27.92, 50.40, 59.91, 84.40))
    powers = tpower_GT(loads, 1)
    voms = np.sum(tcost_NGCC_VOM(loads) + tcost_PCC_VOM(loads) + tcost_PCC_compr_VOM(loads))
    prices = np.outer(powers, power_price)
    for ind in range(len(loads)):
        row = prices[ind,:]
        out = np.roll(row,-ind)
        row[...] = out
    prices = np.sum(prices, axis=0)
    return prices - (voms + cost_start_up)
