"""
Modeling module
Declare DAC-air-related constraints.

Pengfei Cheng

1. state equation
2. continuity of states
3. initial conditions
4. end conditions
5. CO2 capture
6. steam usage
7. power usage
8. mass balance inequalities
"""

from pyomo.environ import *
from ..pyomo_model.params import *


    #TODO: emulate following 4 sections in constraints
    ## 1. STATE EQUATION
    ## x_sorbent_A1
    #def eq_A1_state(m, i, j):
    #    return m.x_sorbent_A1[i, j + 1] == m.x_sorbent_A0[i, j]
    #m.eq_A1_state = Constraint(set_hour_0, set_quarter, rule=eq_A1_state)
    ## x_sorbent_F
    #def eq_f_state(m, i, j):
    #    return m.x_sorbent_F[i, j + 1] == m.x_sorbent_F[i, j] - m.x_sorbent_A0[i, j] + m.x_sorbent_R[i, j]
    #m.eq_f_state = Constraint(set_hour_0, set_quarter, rule=eq_f_state)
    ## x_sorbent_S
    #def eq_s_state(m, i, j):
    #    return m.x_sorbent_S[i, j + 1] == m.x_sorbent_S[i, j] - m.x_sorbent_R[i, j] + m.x_sorbent_A1[i, j]
    #m.eq_s_state = Constraint(set_hour_0, set_quarter, rule=eq_s_state)

    ## --------------------------------------------------------------------------

    ## 2. CONTINUITY OF STATES
    ## connect the ending slice with the beginning slice of the next hour

    ## x_sorbent_A1
    #def eq_A1_cont(m, i):
    #    return m.x_sorbent_A1[i, 0] == m.x_sorbent_A1[i - 1, n_slice]
    #m.eq_A1_cont = Constraint(set_hour, rule=eq_A1_cont)
    ## x_sorbent_F
    #def eq_F_cont(m, i):
    #    return m.x_sorbent_F[i, 0] == m.x_sorbent_F[i - 1, n_slice]
    #m.eq_F_cont = Constraint(set_hour, rule=eq_F_cont)
    ## x_sorbent_S
    #def eq_S_cont(m, i):
    #    return m.x_sorbent_S[i, 0] == m.x_sorbent_S[i - 1, n_slice]
    #m.eq_S_cont = Constraint(set_hour, rule=eq_S_cont)

    ## --------------------------------------------------------------------------

    ## 3. INITIAL CONDITIONS
    #def eq_A1_init(m):
    #    return m.x_sorbent_A1[0, 0] == 0
    #m.eq_A1_init = Constraint(rule=eq_A1_init)
    #def eq_F_init(m):
    #    return m.x_sorbent_F[0, 0] == m.x_sorbent_total
    #m.eq_F_init = Constraint(rule=eq_F_init)
    #def eq_S_init(m):
    #    return m.x_sorbent_S[0, 0] == 0
    #m.eq_S_init = Constraint(rule=eq_S_init)

    ## --------------------------------------------------------------------------

    ## 4. END CONDITIONS
    #def eq_A1_end(m):
    #    return m.x_sorbent_A1[n_hour, n_slice] == 0
    #m.eq_A1_end = Constraint(rule=eq_A1_end)
    #def eq_f_end(m):
    #    return m.x_sorbent_F[n_hour, n_slice] == m.x_sorbent_total
    #m.eq_f_end = Constraint(rule=eq_f_end)
    #def eq_s_end(m):
    #    return m.x_sorbent_S[n_hour, n_slice] == 0
    #m.eq_s_end = Constraint(rule=eq_s_end)

    # --------------------------------------------------------------------------

    # 5. CO2 capture
    #def eq_CO2_DAC(m, i, j):
    #    return m.x_CO2_DAC[i, j] == sorbent_cap_DAC_air * m.x_sorbent_R[i, j]
    #m.eq_CO2_DAC = Constraint(set_hour_0, set_quarter, rule=eq_CO2_DAC)
def dCO2_DAC(dsorbent_A):
    return sorbent_cap_DAC_air * dsorbent_A

    # --------------------------------------------------------------------------

    # 6. STEAM USAGE
    #def eq_steam_DAC(m, i, j):
    #    return m.x_steam_DAC[i, j] == a_steam_DAC * sorbent_cap_DAC_air * m.x_sorbent_R[i, j]
    #m.eq_steam_DAC = Constraint(set_hour_0, set_quarter, rule=eq_steam_DAC)
def dsteam_DAC(dsorbent_A):
    return a_steam_DAC * sorbent_cap_DAC_air * dsorbent_A

    # --------------------------------------------------------------------------

    # 7. POWER USAGE
    #def eq_power_DAC(m, i, j):
    #    return m.x_power_DAC[i, j] == a_power_DAC * sorbent_cap_DAC_air * (m.x_sorbent_A0[i, j] + m.x_sorbent_A1[i, j]) / 2
    #m.eq_power_DAC = Constraint(set_hour_0, set_quarter, rule=eq_power_DAC)
def dpower_DAC(dsorbent_A):
    return a_power_DAC * sorbent_cap_DAC_air * dsorbent_A

    # --------------------------------------------------------------------------

    #TODO: move to constraints
    # 8. MASS BALANCE INEQUALITIES
    #def eq_A0_limit(m, i, j):
    #    return m.x_sorbent_A0[i, j] <= m.x_sorbent_F[i, j]
    #m.eq_A0_limit = Constraint(set_hour_0, set_quarter, rule=eq_A0_limit)
    #def eq_R_limit(m, i, j):
    #    return m.x_sorbent_R[i, j] <= m.x_sorbent_S[i, j]
    #m.eq_R_limit = Constraint(set_hour_0, set_quarter, rule=eq_R_limit)

