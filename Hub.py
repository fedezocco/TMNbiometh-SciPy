"""Implemented by Federico Zocco
    Last update: 14 November 2022
    
Implementation of the biomass hub as detailed in [1].

References:
    [1] Zocco, F., Sopasakis, P., Smyth, B., and 
    Haddad, W.M., 2022. Thermodynamical Material Networks for 
    Modeling, Planning, and Control of Circular Material 
    Flows. arXiv preprint arXiv:2111.10693.
"""


import matplotlib.pyplot as plt

# Parameters:
m_1_ini = 5000
n_l = 7
m_l = 200
n_final = 15

# Discrete-time dynamics:
m_1_current = m_1_ini
m_1_new = [None]*n_final

for n in range(n_final):
    if n != n_l:
        m_1_new[n] = m_1_current
    else:
        m_1_new[n] = m_1_current - m_l
    m_1_current = m_1_new[n] 
            

# Plot:
fig = plt.figure(figsize=(10, 10))
plt.plot(range(n_final), m_1_new, 'm-', linewidth=6)
plt.grid()
plt.xlabel(r"Time, $n$", fontsize=35)
plt.ylabel(r"Hub biomass stock, $m_1$ $\left(kg \right)$", fontsize=35) 
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)                