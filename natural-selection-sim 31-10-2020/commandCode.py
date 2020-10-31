import os
import pickle
from abc import ABC, abstractmethod
import organisms
from vectorMath import Vector
import math
import random

#todo create multi add feature
#todo change createAnimal to type int


# background code. need not write into a class
def decipherAnimal(name):
    try:
        with open("organisms/{0}.oa".format(name), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("organisms/{0}.oa cannot be found. Please ensure your code is correct".format(name))
        exit()


def decipherMap(name):
    try:
        with open("map/{0}._map".format(name), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("map/{0}._map cannot be found. Please ensure your code is correct".format(name))
        exit()

def decipherPlant(name):
    try:
        with open("organisms/{0}.op".format(name), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("organisms/{0}.op cannot be found. Please ensure your code is correct".format(name))
        exit()


def getRandomLocation(distance, objs):
    location = [i.pos for i in objs]
    r = random.randint(1, distance)
    theta = math.radians(random.randint(0, 359))
    x = round(r * math.cos(theta))
    y = round(r * math.sin(theta))
    path = Vector(x, y)
    while path in location:
        path.x += random.randint(-1, 1)
        path.y += random.randint(-1, 1)
    return path


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
    def __init__(self, *args):
        # order = energy, growthRate, attractiveness, expectations, vision, species, foodEat
        super().__init__()
        self.energy = args[0]
        self.growthRate = args[1]
        self.attractiveness = args[2]
        self.expectations = args[3]
        self.vision = args[4]
        self.species = args[5]
        self.foodEat = args[6].split(",")

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
        print("successfully created an animal with above stats")


class createMap(code):
    def __init__(self, *args, mapContent=None):
        if mapContent is None:
            mapContent = []
        super().__init__()
        try:
            self.name = args[0]
        except IndexError:
            print("A name for the map isnt specified. Default map name is used")
            self.name = "you-are-lazy"
        self.mapContent = mapContent

    def run(self):
        if not self.mapContent:
            print("creating a ._map file with name {0}".format(self.name))
        else:
            print("editing a ._map file with name {0}".format(self.name))
        self.name += "._map"
        with open("map/" + self.name, "wb") as f:
            pickle.dump(self.mapContent, f)


class addAnimal(code):
    def __init__(self, *args):
        # order = nameMap, species, location
        super().__init__()
        self.nameMap = args[0]
        self.nameOrganism = args[1]
        location = args[2].split(",")
        self.location = Vector(int(location[0]), int(location[1]))

    def run(self):
        _map = decipherMap(self.nameMap)
        organism = decipherAnimal(self.nameOrganism)
        gender = random.choice(["M", "F"])
        organism = organisms.animal(self.location, organism["energy"], organism["growthRate"], organism["attractiveness"]
                                        , organism["expectations"], organism["vision"], organism["species"],
                                        organism["foodEat"]
                                        , gender)
        _map.append(organism)
        runCode = createMap(self.nameMap,mapContent=_map)
        runCode.run()

class addPlant(code):
    def __init__(self,*args):
        #nameMap, species,location
        super().__init__()
        self.nameMap = args[0]
        self.nameOrganism = args[1]
        location = args[2].split(",")
        self.location = Vector(int(location[0]), int(location[1]))

    def run(self):
        _map = decipherMap(self.nameMap)
        organism = decipherPlant(self.nameOrganism)
        organism = organisms.plant(self.location, organism["energy"], organism["spread"], organism["growthRate"]
                                   , organism["species"], organism["reproduceRate"])
        _map.append(organism)
        runCode = createMap(self.nameMap,mapContent=_map)
        runCode.run()

class createPlant(code):
    def __init__(self, *args):
        # order = energy, spread, growthRate, species, reproduceRate
        super().__init__()
        self.energy = args[0]
        self.spread = args[1]
        self.growthRate = args[2]
        self.species = args[3]
        self.reproduceRate = args[4]

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
    def __init__(self, *args):
        super(deleteAnimal, self).__init__()
        self.name = args[0]

    def run(self):
        os.remove("organisms/{0}.oa".format(self.name))


class deletePlant(code):
    def __init__(self, *args):
        super(deletePlant, self).__init__()
        self.name = args[0]

    def run(self):
        os.remove("organisms/{0}.op".format(self.name))


class deleteMap(code):
    def __init__(self, *args):
        super(deleteMap, self).__init__()
        self.name = args[0]

    def run(self):
        print("deleting map/{0}._map".format(self.name))
        try:
            os.remove("map/{0}._map".format(self.name))
        except WindowsError:
            print("The ._map file you are trying to delete is non-existent")


class printMap(code):
    def __init__(self, *args):
        super().__init__()
        self.name = args[0]

    def run(self):
        _map = (decipherMap(self.name))
        print("this is the map: ")
        for i in _map:
            print(i)


class run(code):
    def __init__(self, *args):
        # order = name, times
        super().__init__()
        self.name = args[0]
        self.times = args[1]

    def run(self):
        map = decipherMap(self.name)
        for i in map:
            map = i.move(map)
        createMap(self.name, mapContent=map)
