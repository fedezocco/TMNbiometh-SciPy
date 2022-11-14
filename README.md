# A SciPy Implementation of a Three-Compartment Bio-Methane TMN

Source code of the paper: 
Zocco, F., Sopasakis, P., Smyth, B., and Haddad, W.M., 2022. Thermodynamical Material Networks for Modeling, Planning, and Control of Circular Material Flows. arXiv preprint arXiv:2111.10693. 

As suggested by the paper title, the main goal of the paper is to propose a generalized and systematic methodology based on compartmental dynamical thermodynamics and graph theory to re-design material flows. The key idea is to see any supply chain as the result of multiple thermodynamical compartments connected through the exhcange of materials; the connections and the compartments can be added, removed and modified as appropriate at the design stage to analyze different scenarios. This is possible thanks to the generality of thermodynamics, which has been developed for chemical, electrical, mechanical and thermal systems in the past. These systems are the backbone of the industrial networks we have today. A summary of the proposed methodology is below.

![Capture](https://user-images.githubusercontent.com/62107909/201691875-f3537b11-ca5b-4ca0-8320-008b575b5a0e.JPG)


To demonstrate the applicability of the methodology, we considered the small bio-methane supply chain below. The code in this repository was used to generate the numerical results for this three-compartment bio-methane network. 

![Capture](https://user-images.githubusercontent.com/62107909/201692719-a61faa3c-79b4-4e28-88be-8cf1ecb2dac0.JPG)





## Code overview
The folder contains four independent scripts: one for the truck, one for the digester in open loop, one for the digester in closed loop, and one for the biomass hub.

Nomenclature used for the state space formulation of the truck:

![Nomenclature_truck_res](https://user-images.githubusercontent.com/62107909/180830194-156bd004-1ac8-445c-b011-45d97f860098.JPG)


Nomenclature used for the state space formulation of the anaerobic digester in closed loop (the same for the open loop except that the original variables are NOT translated):

![Translated_digester_closedLoop_res](https://user-images.githubusercontent.com/62107909/180830819-2fafeb5f-2605-4c5d-b253-3cc3c3ab4477.JPG)


Variables with "bar" correspond to the desired equilibrium, which is the point SS6 here.  





## Graph-based circularity indicator
Leveraging the definition of TMNs, we also develop a material flow circularity indicator and illustrate its calculation for the network below. See the source paper for details.

![Capture](https://user-images.githubusercontent.com/62107909/201694995-1e550278-8b28-4988-808e-a74f3d9f4f60.JPG)
