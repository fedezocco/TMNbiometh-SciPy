"""Implemented by Federico Zocco
   Last update: 17 April 2023
   
   Simulation of the entries of the discrete-time Gamma shown
   in Fig. 9 of [1].
   
   References:
       [1] Zocco, F., Sopasakis, P., Smyth, B., and 
       Haddad, W.M., 2022. Thermodynamical Material Networks for 
       Modeling, Planning, and Control of Circular Material 
       Flows. arXiv preprint arXiv:2111.10693.
       [2] Kaminski, D. A., and M. K. Jensen. 2017. 
       Introduction to Thermal and Fluids Engineering. 
       United States: John Wiley & Sons
"""

from IPython import get_ipython
get_ipython().magic('reset -sf') # Clear all
###

import matplotlib.pyplot as plt

#######################Simulator setting#####################
T = 2 # sample time
t_final = 80
n_l = 7
t_u = 60
m_l = 200
m_1 = 5000 # initial value
mDot_12 = 0 # initial value
m_p = 0 # initial value 
############################################

n_final = int(t_final/T)
t_l = T*n_l  
n_u = t_u/T
m_1new = [None]*n_final
mDot_12new = [None]*n_final 
m_pnew = [None]*n_final
mDot_21new = [None]*n_final

for n in range(n_final):
    # Evaluate the delta:
    if n == n_l:
        delta_nl = 1 
    else:     
        delta_nl = 0
        
    if n == n_u:
        delta_nu = 1 
    else:     
        delta_nu = 0
        
    # m_1 update:
    m_1new[n] = m_1 - delta_nl*m_l
    m_1 = m_1new[n]
    
    # mDot_12 update:
    mDot_12new[n] = mDot_12 + (delta_nl - delta_nu)*(m_l/(t_u-t_l))
    mDot_12 = mDot_12new[n] 
    
    # m_p update:
    m_pnew[n] = m_p + delta_nu*m_l
    m_p = m_pnew[n]
    
    # mDot_21 update:
    mDot_21new[n] = 0
    mDot_21 = mDot_21new[n]  


# Plots:
fig = plt.figure(figsize=(10, 10))
plt.plot(range(n_final), m_1new, 'm*', markersize=12)
plt.grid()
plt.xlabel(r"Time, $n$", fontsize=35)
plt.ylabel(r"Hub biomass stock, $m_1$ $\left(kg \right)$", fontsize=35) 
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)

fig = plt.figure(figsize=(10, 10))
plt.plot(range(n_final), mDot_12new, 'b*', markersize=12)
plt.grid()
plt.xlabel(r"Time, $n$", fontsize=35)
plt.ylabel(r"Truck mass flow rate, $\dot{m}_{1,2}$ $\left(kg/s \right)$", fontsize=35) 
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)

fig = plt.figure(figsize=(10, 10))
plt.plot(range(n_final), m_pnew, 'k*', markersize=12)
plt.grid()
plt.xlabel(r"Time, $n$", fontsize=35)
plt.ylabel(r"Digestion plant stock, $m_p$ $\left(kg \right)$", fontsize=35) 
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)

fig = plt.figure(figsize=(10, 10))
plt.plot(range(n_final), mDot_21new, 'g*', markersize=12)
plt.grid()
plt.xlabel(r"Time, $n$", fontsize=35)
plt.ylabel(r"Not-existing flow, $\dot{m}_{2,1}$ $\left(kg/s \right)$", fontsize=35) 
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)