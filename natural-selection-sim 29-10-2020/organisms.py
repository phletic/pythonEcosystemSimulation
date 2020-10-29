import sys
from abc import ABC, abstractmethod
# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from vectorMath import Vector
import random
import math

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
        self.pos = pos
        self.energy = energy
        self.growthRate = growthRate
        self.vision = vision
        self.species = name
        self.age = 0
        self.type = type

    def __repr__(self):
        return self.species + "\t" + str(self.pos) + "\t" + str(self.energy) + "\t" + str(self.age)

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
        self.currentPath = []
        self.indexInCurrentPath = 0
        self.expectations = expectations
        self.foodEat = foodEat
        self.attractiveness = attractiveness
        self.notMate = notMate
        super().__init__(pos, energy, growthRate, vision, species, "animal")

    # That one annoying a star program
    def aStar(self, end, obstacle):
        """
        :param end:
        :param obstacle:
        :return:
        """
        start = self.pos
        _open = [Node(self.pos, 0)]
        close = []
        previousOptions = [Node(self.pos, 0)]
        total = 0
        while True:
            minVal, index = sys.maxsize, 0
            for e, i in enumerate(previousOptions):
                if i.f < minVal:
                    minVal = i.f
                    index = e
            q = previousOptions[index]
            newLocations = [q.v + Vector(1, 0), q.v + Vector(0, 1),
                            q.v + Vector(0, -1), q.v + Vector(-1, 0)]
            newLocations = [Node(i, 0) for i in newLocations]
            previousOptions.clear()
            for i in newLocations:
                shouldSkip = False
                for k in obstacle:
                    if i.v == k:
                        shouldSkip = True
                if shouldSkip:
                    continue
                if i.v == end:
                    close.append(q)
                    close.append(Node(end, 0))
                    result = []
                    for j in close:
                        result.append(j.v)
                    result = result[1:]
                    return result
                shouldSkip = False
                for j in _open:
                    if j.v == i.v:
                        shouldSkip = True
                for z in close:
                    if z.v == i.v:
                        shouldSkip = True
                if shouldSkip:
                    continue
                else:
                    i.f = Vector.Distance(i.v, end) + Vector.Distance(i.v, start)
                    _open.append(i)
                    previousOptions.append(i)

            thingToRemove = q
            for e, i in enumerate(_open):
                if str(i) == str(thingToRemove):
                    index = e
            close.append(q)
            _open.pop(index)
            total += 1

    def reproduce(self, _map, partner, vision):
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
        newPos = self.getRandomLocation(2, vision)
        Baby = animal(newPos, newEnergy, newGrowthRate,
                      newAttractiveness, newExpectations, newVision, self.species, self.foodEat,
                      newGender, notMate=[self, partner])
        self.notMate.append(partner)
        partner.wait = False
        _map.append(Baby)
        return _map

    def go(self, vision, _map):
        newPos = self.currentPath[self.indexInCurrentPath]
        for i in vision:
            if i.pos == newPos:
                if i.species in self.foodEat:
                    self.currentPath = []
                    self.indexInCurrentPath = 0
                    self.pos = newPos
                    i.die(_map)
                    self.energy += i.energy
                    break
                if i.species == self.species:
                    if i.gender is not self.gender and self.expectations >= i.attractiveness and i.check(self) is True \
                            and i not in self.notMate:
                        _map = self.reproduce(_map, i, vision)
                        break
                    else:
                        self.currentPath = []
                        self.indexInCurrentPath = 0
                        _map = self.move(_map)
                        break
        else:
            if newPos == self.currentPath[-1]:
                self.currentPath = []
                self.indexInCurrentPath = 0
                self.pos = newPos
                self.energy += 1
                self.age -= self.growthRate
                self.move(_map)
            else:
                self.pos = newPos
                self.indexInCurrentPath += 1
        return _map

    def move(self, _map):
        #todo. redo the move script AGAIN!!!! WHY!!!! I DONT KNOW.... IM GOING INSANE
        pass
    def check(self, other):
        if self.expectations >= other.attractiveness:
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
    rabbit = animal(Vector(2, 2), 10, 2, 5, 10, 10, "rabbit", ["grass"], "M")
    fox = animal(Vector(0, 0), 10, 2, 5, 10, 10, "fox", ["rabbit"], "M")
    _map = [rabbit, fox]
    while True:
        input("")
        for i in _map:
            _map = i.move(_map)
        print(_map)
