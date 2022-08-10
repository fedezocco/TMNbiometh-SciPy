# A SciPy Implementation of a Seven-Compartment Bio-Methane TMN

Source code of the paper: 
Zocco, F., Sopasakis, P., Haddad, W.M. and Smyth, B., 2022. Thermodynamical Material Networks for Modeling, Planning and Control of Circular Material Flows. arXiv preprint arXiv:2111.10693. The paper will be submitted in the next few days.




## Code overview
The folder contains three independent scripts: one to simulate the truck, one to simulate the digester in open loop and one to simulate the digester in closed loop as described in the source paper.

Nomenclature used for the state space formulation of the truck:

![Nomenclature_truck_res](https://user-images.githubusercontent.com/62107909/180830194-156bd004-1ac8-445c-b011-45d97f860098.JPG)


Nomenclature used for the state space formulation of the anaerobic digester in closed loop (the same for the open loop except that the original variables are NOT translated):

![Translated_digester_closedLoop_res](https://user-images.githubusercontent.com/62107909/180830819-2fafeb5f-2605-4c5d-b253-3cc3c3ab4477.JPG)


Variables with "bar" correspond to the desired equilibrium, which is the point SS6 here.

Note that, while the network in total has 7 compartments, only the 3 dynamical compartments are implemented (i.e. the 2 trucks and the anaerobic digester with and without the controller). Refer to the source paper for the ordinary differential equations.   
