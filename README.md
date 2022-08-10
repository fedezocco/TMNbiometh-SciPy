# A SciPy Implementation of a Seven-Compartment Bio-Methane TMN

Source code of the paper: 
Zocco, F., Sopasakis, P., Haddad, W.M. and Smyth, B., 2022. Thermodynamical Material Networks for Modeling, Planning and Control of Circular Material Flows. arXiv preprint arXiv:2111.10693. 

As suggested by the paper title, the main goal of the paper is to propose a generalized and systematic methodology based on compartmental dynamical thermodynamics and graph theory to re-design material flows. The key idea is to see any supply chain as the result of multiple thermodynamical compartments connected through the exhcange of materials; the connections and the compartments can be added, removed and modified as appropriate at the design stage to analyze different scenarios. This is possible thanks to the generality of thermodynamics which has been developed for chemical, electrical, mechanical and thermal systems in the past. These systems are the backbone of the industrial networks we have today. A summary of the proposed methodology is below.

![Capture2](https://user-images.githubusercontent.com/62107909/183888447-470f25de-0b4d-41e0-9725-0c0fd103ad34.JPG)

To demonstrate the applicability of the methodology, we considered the small bio-methane supply chain below. The code in this repository was used to generate the numerical results for this seven-compartment bio-methane network. 

![Capture](https://user-images.githubusercontent.com/62107909/183885363-2bdfe96f-962e-4e4d-9b4a-e1a560ad6bf7.JPG)





## Code overview
The folder contains three independent scripts: one to simulate the truck, one to simulate the digester in open loop and one to simulate the digester in closed loop as described in the source paper.

Nomenclature used for the state space formulation of the truck:

![Nomenclature_truck_res](https://user-images.githubusercontent.com/62107909/180830194-156bd004-1ac8-445c-b011-45d97f860098.JPG)


Nomenclature used for the state space formulation of the anaerobic digester in closed loop (the same for the open loop except that the original variables are NOT translated):

![Translated_digester_closedLoop_res](https://user-images.githubusercontent.com/62107909/180830819-2fafeb5f-2605-4c5d-b253-3cc3c3ab4477.JPG)


Variables with "bar" correspond to the desired equilibrium, which is the point SS6 here.

Note that, while the network in total has 7 compartments, only the 3 dynamical compartments are implemented (i.e. the 2 trucks and the anaerobic digester with and without the controller). Refer to the source paper for the ordinary differential equations and the controller design.   
