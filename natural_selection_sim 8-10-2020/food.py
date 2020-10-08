from abc import ABC, abstractmethod
from vectorMath import Vector


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


class plant(food):
    def start(self):
        self.type = 'plant'
