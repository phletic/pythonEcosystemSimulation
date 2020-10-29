import os
import pickle
from abc import ABC, abstractmethod


# background code. need not write into a class
def decipherAnimal(name):
    with open("organisms/{0}.oa".format(name), "rb") as f:
        return pickle.load(f)


def decipherMap(name):
    with open("map/{0}._map".format(name), "rb") as f:
        return pickle.load(f)


def decipherPlant(name):
    with open("organisms/{0}.op".format(name), "rb") as f:
        return pickle.load(f)


# --------------------------------------------
# BASE CLASS
class code(ABC):
    def __init__(self):
        super().__init__()

    # driver code will call the run function
    @abstractmethod
    def run(self):
        pass


# children
class createAnimal(code):
    def __init__(self, energy, growthRate, attractiveness, expectations, vision, species, foodEat):
        super().__init__()
        self.energy = energy
        self.growthRate = growthRate
        self.attractiveness = attractiveness
        self.expectations = expectations
        self.vision = vision
        self.species = species.split(",")
        self.foodEat = foodEat

    def run(self):
        stats = {}
        stats["energy"] = self.energy
        stats["growthRate"] = self.growthRate
        stats["attractiveness"] = self.attractiveness
        stats["expectations"] = self.expectations
        stats["vision"] = self.vision
        stats["species"] = self.species
        stats["foodEat"] = self.foodEat
        name = "{0}.oa".format(self.species)
        with open("organisms/" + name, "wb") as f:
            pickle.dump(stats, f)


class createMap(code):
    def __init__(self, name, mapContent=None):
        if mapContent is None:
            mapContent = []
        super().__init__()
        self.name = name
        self.mapContent = mapContent

    def run(self):
        self.name += "._map"
        with open("map/" + self.name, "wb") as f:
            pickle.dump(self.mapContent, f)


class addOraganism(code):
    def __init__(self, nameMap, nameOrganism, type):
        super().__init__()
        self.nameMap = nameMap
        self.nameOrganism = nameOrganism
        self.type = type

    def run(self):
        organism = decipherAnimal(self.nameOrganism) if self.type == "animal" else decipherPlant(self.nameOrganism)
        map = decipherMap(self.nameMap)
        map += organism
        createMap(self.nameMap, mapContent=map)


class createPlant(code):
    def __init__(self, energy, spread, growthRate, species, reproduceRate):
        super().__init__()
        self.energy = energy
        self.spread = spread
        self.growthRate = growthRate
        self.species = species
        self.reproduceRate = reproduceRate

    def run(self):
        stats = {}
        stats["energy"] = self.energy
        stats["spread"] = self.spread
        stats["growthRate"] = self.growthRate
        stats["species"] = self.species
        stats["reproduceRate"] = self.reproduceRate
        name = "{0}.op".format(self.species)
        with open("organisms/" + name, "wb") as f:
            pickle.dump(stats, f)


class deleteAnimal(code):
    def __init__(self, name):
        super(deleteAnimal, self).__init__()
        self.name = name

    def run(self):
        os.remove("organisms/{0}.oa".format(self.name))


class deletePlant(code):
    def __init__(self, name):
        super(deletePlant, self).__init__()
        self.name = name

    def run(self):
        os.remove("organisms/{0}.op".format(self.name))


class printMap(code):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(decipherMap(self.name))


class run(code):
    def __init__(self, name, times):
        super().__init__()
        self.name = name
        self.times = times

    def run(self):
        map = decipherMap(self.name)
        for i in range(self.times):
            for item in map:
                map = item.move(map)
        createMap(self.name, mapContent=map)
