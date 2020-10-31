import math
import random
import string
import sys
from abc import ABC, abstractmethod

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from vectorMath import Vector

'''
This program will store all the animal classes.
I hope I will be able to allow the user to create his own organisms with custom behaviors AKA edit the program through a UI
'''


# This Node is for the a* algorithm. THe Repr method is pretty useless as I wouldn't print it but still I guess no harm keeping...
class Node:
    """

    """

    def __init__(self, v, f):
        self.v = v
        self.f = f

    def __repr__(self):
        return f"{self.v},{self.f}"


class organisms(ABC):
    """

    """

    def __init__(self, pos, energy, growthRate, vision, name, type):
        self.id = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        self.pos = pos
        self.energy = energy
        self.growthRate = growthRate
        self.vision = vision
        self.species = name
        self.age = 0
        self.type = type

    def __repr__(self):
        return self.species + "\t" + str(self.pos) + "\tenergy:" + str(self.energy) + "\tage:" + str(self.age) + "\tid:" + self.id

    def getRandomLocation(self, distance, objs):
        location = [i.pos for i in objs]
        r = random.randint(1, distance)
        theta = math.radians(random.randint(0, 359))
        x = round(r * math.cos(theta) + self.pos.x)
        y = round(r * math.sin(theta) + self.pos.y)
        path = Vector(x, y)
        while path in location:
            path.x += random.randint(-1, 1)
            path.y += random.randint(-1, 1)
        return path

    def die(self, _map):
        """

        :param map: list
        :return: map
        """
        _map.remove(self)
        return _map

    @abstractmethod
    def move(self, _map):
        pass


# animal class. the parent
class animal(organisms):
    """

    animals: Rules: When it run the move() function, it picks out all organisms in the area within its vision. If
    there is another organism of differing gender, it will check if its expectations > other species attractiveness
    and vice versa. When both conditions pass, it will mate

    """

    # noinspection PyCompatibility
    def __init__(self, pos: Vector, energy: int, growthRate: int, attractiveness: int, expectations: int, vision: int,
                 species: str, foodEat: list,
                 gender: str,
                 notMate: list = None):
        if notMate is None:
            notMate = []
        self.wait = False
        self.gender = gender
        self.expectations = expectations
        self.foodEat = foodEat
        self.attractiveness = attractiveness
        self.notMate = notMate
        super().__init__(pos, energy, growthRate, vision, species, "animal")

    # That one annoying a star program -- which in the end I had to redo
    def alteredPathFindingAlgo(self, end, obstacle):
        locations = [i.pos for i in obstacle]
        possibleLocations = [Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]
        possibleLocations = [Node(v=(i + self.pos), f=(
                Vector.Distance(i + self.pos, end) + Vector.Distance(self.pos, i + self.pos))) for i in
                             possibleLocations if i not in locations]
        lowestF, index = sys.maxsize, 0
        for e, i in enumerate(possibleLocations):
            if i.f < lowestF:
                lowestF = i.f
                index = e
        return possibleLocations[index].v

    def reproduce(self, _map, partner):
        # since B < A, I will do sth horrendous so that the random function will not have a A < B scenario
        # This code determine the stats of the baby
        # the creature will not mate with the immediate parents
        newEnergy = random.randint(self.energy, partner.energy) if partner.energy > self.energy else random.randint(
            partner.energy, self.energy)
        newGrowthRate = random.randint(self.growthRate,
                                       partner.growthRate) if partner.growthRate > self.growthRate else random.randint(
            partner.growthRate, self.growthRate)
        newAttractiveness = random.randint(self.attractiveness,
                                           partner.attractiveness) if partner.attractiveness > self.attractiveness else random.randint(
            partner.attractiveness, self.attractiveness)
        newExpectations = random.randint(self.expectations,
                                         partner.expectations) if partner.expectations > self.expectations else random.randint(
            partner.expectations, self.expectations)
        newVision = random.randint(self.vision, partner.vision) if partner.vision > self.vision else random.randint(
            partner.vision, self.vision)
        newGender = random.choice(["M", "F"])
        newPos = self.getRandomLocation(2, _map)
        Baby = animal(newPos, newEnergy, newGrowthRate,
                      newAttractiveness, newExpectations, newVision, self.species, self.foodEat,
                      newGender, notMate=[self, partner])
        self.notMate.append(partner)
        self.notMate.append(Baby)
        partner.notMate.append(self)
        partner.notMate.append(Baby)
        partner.wait = False
        _map.append(Baby)
        return _map

    def move(self, _map):
        self.energy -= 1;
        self.age += self.growthRate
        if self.energy <= 0 or self.age >= 100:
            _map = self.die(_map)
            return _map
        locations = [i for i in _map if Vector.Distance(i.pos, self.pos) < self.vision and i.pos is not self.pos]
        lowestDistance, index = sys.maxsize, 0
        possibleLocations = []
        for e, i in enumerate(locations):
            distance = Vector.Distance(self.pos, i.pos)
            if i.type == "animal":
                if self.species in i.foodEat:
                    # Im prey I should run
                    possibleLocations.append(self.pos - i.pos + self.pos)
                if i.species is self.species and i not in self.notMate and self not in i.notMate:
                    if self.check(i) and i.check(self):
                        # Im mate
                        if distance <= 1:
                            print("reproduce")
                            _map = self.reproduce(_map, i)
                            return _map
                        possibleLocations.append(i.pos)
            if i.species in self.foodEat:
                # Im predator I should chase
                if distance <= 1:
                    self.energy += i.energy
                    _map = i.die(_map)
                    print("eat")
                    return _map
                possibleLocations.append(i.pos)

            if distance < lowestDistance:
                lowestDistance = distance
                index = e
        if not possibleLocations:
            possibleLocations.append(self.getRandomLocation(self.vision, _map))
            index = 0
        global path
        try:
            path = self.alteredPathFindingAlgo(possibleLocations[index], _map)
        except Exception as e:
            print(possibleLocations, index, self, e)
            exit()
        self.pos = path
        return _map

    def check(self, other):
        if self.expectations <= other.attractiveness:
            return True
        else:
            return False


class plant(organisms):
    """

    """

    def __init__(self, pos, energy, spread, growthRate,
                 species, reproduceRate):  # vision = spread of plant - how far it can produce new of itself
        """
        :param pos:
        :param energy:
        :param vision:
        :param growthRate:
        :param species:
        """
        self.reproduceRate = reproduceRate
        # noinspection PyCompatibility
        super().__init__(pos, energy, growthRate, spread, species, "plant")

    def spread(self, _map):
        for i in range(self.reproduceRate):
            location = self.getRandomLocation(self.vision, _map)
            newEnergy = self.energy + random.randint(-2, 2) if self.energy - 2 > 0 else self.energy + random.randint(0,
                                                                                                                     2)
            newSpread = self.vision + random.randint(-2, 2) if self.vision - 2 > 0 else self.vision + random.randint(0,
                                                                                                                     2)
            newGrowthRate = self.growthRate + random.randint(-2,
                                                             2) if self.growthRate - 2 > 0 else self.growthRate + random.randint(
                0, 2)
            _map.append(plant(location, newEnergy, newSpread, newGrowthRate, self.species, self.reproduceRate))
        return _map

    def move(self, _map):
        self.age += self.growthRate
        if self.age >= 100:
            _map = self.spread(_map)
            _map = self.die(_map)
        return _map


# for testing puposes only
if __name__ == '__main__':
    rabbit = animal(pos=Vector(5, 2), energy=10, growthRate=10, attractiveness=10, expectations=10, vision=10,
                    species="rabbit", foodEat=["grass"], gender="M")
    rabbitF = animal(pos=Vector(8, 10), energy=10, growthRate=10, attractiveness=10, expectations=10, vision=10,
                     species="rabbit", foodEat=["grass"], gender="F")
    grass = plant(pos=Vector(0, 0), energy=10, spread=5, growthRate=7, species="grass", reproduceRate=10)
    _map = [rabbit, grass, rabbitF]
    while True:
        input("")
        for i in _map:
            _map = i.move(_map)
