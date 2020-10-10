# pythonEcosystemSimulation
The program the host an entire ecosystem


<b>8/10/2020:</b>
1. clases for animal and plants
2. impliment a* algorithm for animals to move around and consume plants for energy. 
3. animals die after losing too much energy (stamina < 0)
4. simple display to see location of ecosystem organisms

<b>10/10/2020:</b>
1. rework the move function of prey child in move.py
 - instead of just finding the nearest food. The animal has limited vision and can only "remember" objects in its vision. It also has a limited memory if there are too many objects to "remember", it will forget some
2. realised I was dumb in not using the super() function in the init function of child. changed that

Diver program : map.py
Diver program : map.py

Current controls:

 - press any button to go to next frame of simulation
 
