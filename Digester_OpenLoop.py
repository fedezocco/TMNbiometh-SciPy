"""Implemented by Federico Zocco
    Last update: 14 November 2022
    
Implementation of the anaerobic digester in open loop
as detailed in [1], i.e. without the controller in [4].

References:
    [1] Zocco, F., Sopasakis, P., Smyth, B., and 
    Haddad, W.M., 2022. Thermodynamical Material Networks for 
    Modeling, Planning, and Control of Circular Material 
    Flows. arXiv preprint arXiv:2111.10693.
    [2] Campos-Rodríguez, A., García-Sandoval, J.P., 
    González-Álvarez, V. and González-Álvarez, A., 2019. 
    Hybrid cascade control for a class of nonlinear 
    dynamical systems. Journal of Process Control, 76, 
    pp.141-154.
    [3] Bernard, O., Hadj‐Sadok, Z., Dochain, D., Genovesi,
    A. and Steyer, J.P., 2001. Dynamical model development
    and parameter identification for an anaerobic 
    wastewater treatment process. Biotechnology and 
    bioengineering, 75(4), pp.424-438.
    [4] Haddad, W.M. and L'Afflitto, A., 2016. Finite-time
    stabilization and optimal feedback control. IEEE 
    Transactions on Automatic Control, 61(4), pp.1069-1074.
"""

from IPython import get_ipython
get_ipython().magic('reset -sf') # Clear all
###

import numpy as np
import math
from scipy import integrate
import matplotlib.pyplot as plt


#######################Simulator setting#####################
# Model parameters (from Table 2 in [2]):
mu_max1 = 1.2 
mu_max2 = 0.744 
K_S1 = 7.1 
K_S2 = 9.28 
K_I2 = 16 
alpha = 0.5 
k_1 = 42.14 
k_2 = 116.5 
k_3 = 268 
S_1in = 30 
S_2in = 750
k_6 = 453 # value from [3], not [2] 



# Initial conditions:
D_bar = 0.5
S1_ini = (alpha*D_bar*K_S1) / (mu_max1-alpha*D_bar) - 2 
S2_ini = (((K_I2**2)*(mu_max2-alpha*D_bar)) / (2*alpha*D_bar)) - math.sqrt((((K_I2**2)*(mu_max2-alpha*D_bar))/(2*alpha*D_bar))**2 - K_S2*(K_I2**2)) - 1 
X1_ini = (S_1in-S1_ini) / (alpha*k_1) + 2 
X2_ini = (k_2*(S_1in-S1_ini) + k_1*(S_2in-S2_ini)) / (alpha*k_1*k_3) + 1
X_tilde_ini = np.array([X1_ini, S1_ini, X2_ini, S2_ini])

# Inputs (with open loop):
D = D_bar # 0.05 < D < 1.2 for operational stability
################################################################

# Equations in state space form:
def digester_openLoop(X_tilde, t=0): 
    mu1 = mu_max1*(X_tilde[1]/(X_tilde[1] + K_S1))
    mu2 = mu_max2*(X_tilde[3]/(X_tilde[3]+K_S2+(X_tilde[3]/K_I2)**2))  
    
    return np.array([mu1*X_tilde[0] - alpha*X_tilde[0]*D,
                     -k_1*mu1*X_tilde[0] + (S_1in-X_tilde[1])*D,
                     mu2*X_tilde[2] - alpha*X_tilde[2]*D,
                     k_2*mu1*X_tilde[0] - k_3*mu2*X_tilde[2] + (S_2in-X_tilde[3])*D])    


# Numerical solution:
t = np.linspace(0, 14, 1000)
X_tilde, infodict = integrate.odeint(digester_openLoop, X_tilde_ini, t,
mxstep = 1000, full_output = True)
X1, S1, X2, S2 = X_tilde.T


# Biomethane production:
q_M = k_6*mu_max2*(S2/(S2+K_S2+(S2/K_I2)**2))*X2 # equation from [3], not [2]


# Plots
fig = plt.figure(figsize=(25, 15))
fig.subplots_adjust(wspace = 0.5, hspace = 0.3)
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

ax1.plot(t, X1, 'r-', label = 'Acidogenic bacteria')
ax1.set_title("Time Series")
ax1.set_xlabel("time")
ax1.grid()
ax1.legend(loc='best')

ax2.plot(t, S1, 'b-', label = 'Organic substrate')
ax2.set_title("Time Series")
ax2.set_xlabel("time")
ax2.grid()
ax2.legend(loc='best')

ax3.plot(t, X2, 'g-', label = 'Methanogenic bacteria')
ax3.set_title("Time Series")
ax3.set_xlabel("time")
ax3.grid()
ax3.legend(loc='best')

ax4.plot(t, S2, 'k-', label = 'Volatile fatty acids')
ax4.set_title("Time Series")
ax4.set_xlabel("time")
ax4.grid()
ax4.legend(loc='best') 

fig = plt.figure(figsize=(10, 10))
plt.plot(t, q_M, 'm-', linewidth=6)
plt.grid()
plt.xlabel(r"Time, $t$ (d)", fontsize=35)
plt.ylabel(r"Biomethane flow, $q_M$ $\left(\frac{mmol}{Ld}\right)$", fontsize=35) 
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)