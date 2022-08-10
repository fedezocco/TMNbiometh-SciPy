"""Implemented by Federico Zocco
    Last update: 10 August 2022
    
Implementation of the truck as detailed in [1].

References:
    [1] Zocco, F., Sopasakis, P., Haddad, W.M. and Smyth, 
    B., 2022. Thermodynamical Material Networks for 
    Modeling, Planning and Control of Circular Material 
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
# Model parameters:
m_load = 200
m_truck = 3500 
m = m_truck + m_load 
a = 2
b = 3
r = 0.4
l = 2 
I_z = 3000
e = I_z*(r**2/l**2)
d = 0.1
rho = r/d
alpha = (a + b)/l


# Initial conditions:
theta1_ini = 0.0
theta1d_ini = 0.0
theta2_ini = 0.0
theta2d_ini = 0.0
theta3_ini = 0.0
psi_ini = 0.0
X_tilde_ini = np.array([theta1_ini, theta1d_ini, theta2_ini, theta2d_ini, theta3_ini, psi_ini])

    
# Inputs:
tau1 = 10.0 
tau2 = 10.0
tau = np.array([[tau1],[tau2]])
################################################################


# Equations in state space form:
b11 = m*(a**2*r**2/l**2 + r**2/4) + e
b12 = m*(-(a**2*r**2/l**2) + r**2/4) - e
b21 = b12
b22 = b11
B = np.array([[b11,b12],[b21,b22]])
B_inv = np.linalg.inv(B)

    
def truck(X_tilde, t=0): 
    return np.array([X_tilde[1], 
                     np.dot(B_inv[0],tau), 
                     X_tilde[3],
                     np.dot(B_inv[1],tau),
                     np.dot(np.array([(math.cos(X_tilde[5]))/2 - alpha*math.sin(X_tilde[5]), math.cos(X_tilde[5])/2 + alpha*math.sin(X_tilde[5])]), np.array([[X_tilde[1]], [X_tilde[3]]])),
                     np.dot(np.array([rho*(-alpha*math.cos(X_tilde[5]) - (math.sin(X_tilde[5])/2 - d/l)), rho*(alpha*math.cos(X_tilde[5]) - (math.sin(X_tilde[5])/2 + d/l))]), np.array([[X_tilde[1]], [X_tilde[3]]]))], dtype='float64')
                    


# Numerical solution
t = np.linspace(0, 60, 1000)
X_tilde, infodict = integrate.odeint(truck, X_tilde_ini, t,
mxstep=4000, full_output = True)
theta1, theta1d, theta2, theta2d, theta3, psi = X_tilde.T 



# Plots
fig = plt.figure(figsize=(25, 15))
fig.subplots_adjust(wspace = 0.5, hspace = 0.3)
ax1 = fig.add_subplot(3, 2, 1)
ax2 = fig.add_subplot(3, 2, 2)
ax3 = fig.add_subplot(3, 2, 3)
ax4 = fig.add_subplot(3, 2, 4)
ax5 = fig.add_subplot(3, 2, 5)
ax6 = fig.add_subplot(3, 2, 6)

ax1.plot(t, theta1, 'r-', label = 'theta1')
ax1.set_title("Time Series")
ax1.set_xlabel("time")
ax1.grid()
ax1.legend(loc='best')

ax2.plot(t, theta1d, 'b-', label = 'theta1d')
ax2.set_title("Time Series")
ax2.set_xlabel("time")
ax2.grid()
ax2.legend(loc='best')

ax3.plot(t, theta2, 'g-', label = 'theta2')
ax3.set_title("Time Series")
ax3.set_xlabel("time")
ax3.grid()
ax3.legend(loc='best')

ax4.plot(t, theta2d, 'k-', label = 'theta2d')
ax4.set_title("Time Series")
ax4.set_xlabel("time")
ax4.grid()
ax4.legend(loc='best')

ax5.plot(t, theta3, 'k-', label = 'theta3')
ax5.set_title("Time Series")
ax5.set_xlabel("time")
ax5.grid()
ax5.legend(loc='best')

ax6.plot(t, psi, 'k-', label = 'psi')
ax6.set_title("Time Series")
ax6.set_xlabel("time")
ax6.grid()
ax6.legend(loc='best')
plt.show()

# fig = plt.figure(figsize=(10, 10))
# plt.plot(t, theta2, 'r-', label = r'$\theta_2$', linewidth=6)
# plt.plot(t, theta2_doubled, 'b-', label = r'$\theta_2^{new}$', linewidth=6)
# plt.grid()
# plt.legend(loc='best', prop={'size': 27})
# plt.xlabel(r"Time, $t$ (s)", fontsize=35)
# plt.ylabel(r"Angular positions, $\frac{rad}{s}$", fontsize=35)
# plt.xticks(fontsize=35)
# plt.yticks(fontsize=35)