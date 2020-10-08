from abc import ABC, abstractmethod
from vectorMath import Vector

'''
This program is for the plants
'''
#parent
class food(ABC):
    def __init__(self, pos, energy):
        self.pos = pos
        self.type = ''
        self.energy = energy

    def __repr__(self):
        return str(self.pos)

    @abstractmethod
    def start(self):
        pass

#child. like animal, I wanna have some actual plants stemming out of this class
class plant(food):
    def start(self):
        self.type = 'plant'
