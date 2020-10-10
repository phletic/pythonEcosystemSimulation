from abc import ABC, abstractmethod
from vectorMath import Vector


class food(ABC):
    def __init__(self, pos, energy):
        self.pos = pos
        self.energy = energy

    def __repr__(self):
        return self.type + "\t" + str(self.pos) + "\t" + str(self.energy)


class plant(food):
    def __init__(self,pos, energy):
        self.type = 'plant'
        super().__init__(pos,energy)
