"""Implemented by Federico Zocco
    Last update: 14 November 2022
    
Implementation of the truck as detailed in [1] and [2].

References:
    [1] Zocco, F., Sopasakis, P., Smyth, B., and 
    Haddad, W.M., 2022. Thermodynamical Material Networks for 
    Modeling, Planning, and Control of Circular Material 
    Flows. arXiv preprint arXiv:2111.10693.
    [2] Gabiccini, M., 2011. Compito di Robotica I - 01 Aprile 2011. 
    University of Pisa. Available at: http://docenti.ing.unipi.it/gabiccini-m/RAR/01_04_2011.pdf
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
m_l = 200
m_v = 3500 
m = m_v + m_l 
a = 2
b = 3
r = 0.4
l = 2 
I_z = 3000
e = I_z*(r**2/l**2)
d = 0.1
rho = r/d
alpha = (a + b)/l
H = 8000


# Initial conditions:
theta1_ini = 0.0
theta1d_ini = 0.0
theta2_ini = 0.0
theta2d_ini = 0.0
theta3_ini = 0.0
psi_ini = 0.0
X_tilde_ini = np.array([theta1_ini, theta1d_ini, theta2_ini, theta2d_ini, theta3_ini, psi_ini])


# Final time:
t_u = 600  
################################################################


# Equations in state space form:
b11 = m*(a**2*r**2/l**2 + r**2/4) + e
b12 = m*(-(a**2*r**2/l**2) + r**2/4) - e
b21 = b12
b22 = b11
B = np.array([[b11,b12],[b21,b22]])
B_inv = np.linalg.inv(B)


    
def truck(X_tilde, t=0):
    # Control inputs:
    tau = (2*m*r*H)/(t_u**2)
    
    if t < t_u/2:
        tau1 = tau 
        tau2 = tau
    else:
        tau1 = -tau 
        tau2 = -tau
    
    tau_array = np.array([[tau1],[tau2]])
    
    return np.array([X_tilde[1], 
                     np.dot(B_inv[0],tau_array), 
                     X_tilde[3],
                     np.dot(B_inv[1],tau_array),
                     np.dot(np.array([(math.cos(X_tilde[5]))/2 - alpha*math.sin(X_tilde[5]), math.cos(X_tilde[5])/2 + alpha*math.sin(X_tilde[5])]), np.array([[X_tilde[1]], [X_tilde[3]]])),
                     np.dot(np.array([rho*(-alpha*math.cos(X_tilde[5]) - (math.sin(X_tilde[5])/2 - d/l)), rho*(alpha*math.cos(X_tilde[5]) - (math.sin(X_tilde[5])/2 + d/l))]), np.array([[X_tilde[1]], [X_tilde[3]]]))], dtype='float64')
                    


# Numerical solution
t = np.linspace(0, t_u, 1000)
X_tilde, infodict = integrate.odeint(truck, X_tilde_ini, t,
mxstep=4000, full_output = True)
theta1, theta1d, theta2, theta2d, theta3, psi = X_tilde.T 

# Position of biomass center of mass G:
x_G = r*theta1 + a

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

fig = plt.figure(figsize=(10, 10))
plt.plot(t, theta2, 'r-', label = r'$\theta_2$', linewidth=6)
plt.plot(t, x_G, 'b-', label = r'$x_G$', linewidth=6)
plt.grid()
plt.legend(loc='best', prop={'size': 27})
plt.xlabel(r"Time, $t$ (s)", fontsize=35)
plt.ylabel(r"Position", fontsize=35)
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)