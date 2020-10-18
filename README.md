# pythonEcosystemSimulation
The program the host an entire ecosystem

personal document to keep track of program : https://docs.google.com/document/d/1VJ2fTF_HP0MQ0ddz76h636RNew8ycaDu2FV5JCwr2es/edit?usp=sharing


<b>8/10/2020:</b>
1. clases for animal and plants
2. impliment a* algorithm for animals to move around and consume plants for energy. 
3. animals die after losing too much energy (stamina < 0)
4. simple display to see location of ecosystem organisms

<b>10/10/2020:</b>
1. rework the move function of prey child in move.py
 - instead of just finding the nearest food. The animal has limited vision and can only "remember" objects in its vision. It also has a limited memory if there are too many objects to "remember", it will forget some
2. realised I was dumb in not using the super() function in the init function of child. changed that

<b>18/10/2020:</b>
1. I realized the bad design choices of the previous code, so I had to rewrite the animal and plant class codes. Right now, there will be 1 script governing animal and plant behaviours. Details in the google docs
2. Animals can reproduce. When they see a mate, and certain criteria is fulfilled, they will meet and reproduce, spawning a new organism with their attributes a slight variation of their own. 
3. Fixed bugs in the a* system

 
