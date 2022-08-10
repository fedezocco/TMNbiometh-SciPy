"""Implemented by Federico Zocco
    Last update: 10 August 2022
    
Implementation of the anaerobic digester in closed loop
as detailed in [1].

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



# Values at equilibrium SS6 of [2], p. 10 (only D_bar needs to be set):
D_bar = 1.05 # 0.05 < D < 1.2 for operational stability; interval took from [2], p. 11
S1_bar = (alpha*D_bar*K_S1) / (mu_max1-alpha*D_bar)
S2_bar = (((K_I2**2)*(mu_max2-alpha*D_bar)) / (2*alpha*D_bar)) - math.sqrt((((K_I2**2)*(mu_max2-alpha*D_bar))/(2*alpha*D_bar))**2 - K_S2*(K_I2**2))  
X1_bar = (S_1in-S1_bar) / (alpha*k_1)  
X2_bar = (k_2*(S_1in-S1_bar) + k_1*(S_2in-S2_bar)) / (alpha*k_1*k_3)



# Initial conditions:
x1_tilde_ini = 2
x2_tilde_ini = -2
x3_tilde_ini = 1
x4_tilde_ini = -1
X_tilde_ini = np.array([x1_tilde_ini, x2_tilde_ini, x3_tilde_ini, x4_tilde_ini])
################################################################

# Equations in affine state space form:
def digester_closedLoop(X_tilde, t=0): # takes X_tilde as input and returns Xd_tilde
    
    mu1_tilde = mu_max1*((X_tilde[1]+S1_bar) / (X_tilde[1]+S1_bar+K_S1))
    mu2_tilde = mu_max2*((X_tilde[3]+S2_bar) / (X_tilde[3]+S2_bar+K_S2+(((X_tilde[3]+S2_bar)/K_I2)**2)))  
    
    f1 = mu1_tilde*(X_tilde[0]+X1_bar) - alpha*D_bar*(X_tilde[0]+X1_bar) 
    f2 = -k_1*mu1_tilde*(X_tilde[0]+X1_bar) + D_bar*(S_1in-X_tilde[1]-S1_bar)
    f3 = mu2_tilde*(X_tilde[2]+X2_bar) - alpha*D_bar*(X_tilde[2]+X2_bar)
    f4 = k_2*mu1_tilde*(X_tilde[0]+X1_bar) - k_3*mu2_tilde*(X_tilde[2]+X2_bar) + D_bar*(S_2in-X_tilde[3]-S2_bar)                     
    
    f = np.array([[f1],[f2],[f3],[f4]]) 
    
    G11 = - alpha*(X_tilde[0]+X1_bar)
    G22 = S_1in - X_tilde[1] - S1_bar 
    G33 = - alpha*(X_tilde[2]+X2_bar)
    G44 = S_2in - X_tilde[3] - S2_bar
    
    G = np.array([[G11, 0, 0, 0],[0, G22, 0, 0],[0, 0, G33, 0],[0, 0, 0, G44]]) 
    
    # Controller design (set p and expression of V(x)):
    p = 1 # p = 1 from reference [4]
    Vprime = (4/3)*(p**(2/3))*(X_tilde[0]**2+X_tilde[1]**2+X_tilde[2]**2+X_tilde[3]**2)**(-1/3)*np.array([[X_tilde[0], X_tilde[1], X_tilde[2], X_tilde[3]]]) # as in reference [4]
    
    # Control law:
    G_inv = np.linalg.inv(G)
    psi = - (1/2)*G_inv.dot((2*f + Vprime.transpose()))     
                             
    return (f + G.dot(psi)).flatten()    


# Numerical solution:
t = np.linspace(0, 6, 1000)
X_tilde, infodict = integrate.odeint(digester_closedLoop, X_tilde_ini, t,
mxstep=1000, full_output = True)
x1_tilde, x2_tilde, x3_tilde, x4_tilde = X_tilde.T


# Biomethane production (note that S2 = x4_tilde + S2_bar and X2 = x3_tilde + X2_bar):    
q_M = k_6 * mu_max2*((x4_tilde+S2_bar)/(x4_tilde+S2_bar+K_S2+((x4_tilde+S2_bar)/K_I2)**2)) * (x3_tilde+X2_bar) # equation from [3], not [2] 


# Plots
fig = plt.figure(figsize=(10, 10))
plt.plot(t, x1_tilde, 'r-', label = 'Acidogenic bacteria', linewidth=6)
plt.plot(t, x2_tilde, 'b-', label = 'Organic substrate', linewidth=6)
plt.plot(t, x3_tilde, 'g-', label = 'Methanogenic bacteria', linewidth=6)
plt.plot(t, x4_tilde, 'k-', label = 'Volatile fatty acids', linewidth=6)
plt.grid()
plt.legend(loc='best', prop={'size': 27})
plt.xlabel(r"Time, $t$ (d)", fontsize=35)
plt.ylabel(r"Translated state, $\tilde{\mathbf{x}}$", fontsize=35)
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)


fig = plt.figure(figsize=(10, 10))
plt.plot(t, q_M, 'm-', linewidth=6)
plt.grid()
plt.xlabel(r"Time, $t$ (d)", fontsize=35)
plt.ylabel(r"Biomethane flow, $q_M$ $\left(\frac{mmol}{Ld}\right)$", fontsize=35) 
plt.xticks(fontsize=35)
plt.yticks(fontsize=35)
  