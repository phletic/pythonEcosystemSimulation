import sys
from abc import ABC, abstractmethod
# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from vectorMath import Vector
import random
import math

'''
This progam will store all the animal classes.
I hope I will be able to allow the user to create his own organisms with custom behavious AKA edit the program through a UI
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

    '''

    animals: Rules: When it run the move() function, it picks out all organisms in the area within its vision. If
    there is another organism of differing gender, it will check if its expectations > other species attractiveness
    and vice versa. When both conditions pass, it will mate

    '''
    # noinspection PyCompatibility
    def __init__(self, pos, energy, growthRate, attractiveness, expectations, vision, species: str, foodEat, gender,
                 notMate=None):
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
                            q.v + Vector(0, -1), q.v + Vector(-1, 0), q.v + Vector(2, 2)]
            newLocations = [Node(i, 0) for i in newLocations]
            previousOptions.clear()
            for i in newLocations:
                shouldSkip = False
                for k in obstacle:
                    if (i.v == k):
                        shouldSkip = True
                if shouldSkip:
                    continue
                if i.v == end:
                    close.append(q)
                    close.append(Node(end, 0))
                    result = []
                    for j in close:
                        result.append(j.v)
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
    def reproduce(self,_map,partner):
        # since B < A, I will play dirty to do sth horrendous
        # This code determine the stats of the baby
        # the creature will not mate with the immediate parents
        newEnergy = random.randint(self.energy, partner.energy) if partner.energy > self.energy else random.randint(
            partner.energy, self.energy)
        newGrowthRate = random.randint(self.growthRate,
                                       partner.growthRate) if partner.growthRate > self.growthRate else random.randint(
            partner.growthRate, self.growthRate)
        newAttractivness = random.randint(self.attractiveness,
                                          partner.attractiveness) if partner.attractiveness > self.attractiveness else random.randint(
            partner.attractiveness, self.attractiveness)
        newExpectations = random.randint(self.expectations,
                                         partner.expectations) if partner.expectations > self.expectations else random.randint(
            partner.expectations, self.expectations)
        newVision = random.randint(self.vision, partner.vision) if partner.vision > self.vision else random.randint(
            partner.vision, self.vision)
        newGender = random.choice(["M", "F"])
        # todo make sure pos is in a empty location. I'm not sure how I am solving this
        Baby = animal(Vector(self.pos.x + 1, self.pos.y + 1), newEnergy, newGrowthRate,
                      newAttractivness, newExpectations, newVision, self.species, self.foodEat,
                      newGender, notMate=[self, partner])
        self.notMate.append(partner)
        _map.append(Baby)
        return _map
    def go(self, vision, _map):
        newPos = self.currentPath[self.indexInCurrentPath]
        for i in vision:
            if i.pos == newPos:
                if i.species == self.species:
                    if i.gender is not self.gender and self.expectations >= i.attractiveness and i.check(self) is True \
                            and i not in self.notMate:
                        _map = self.reproduce(_map,i)
                        break
                if i.species in self.foodEat:
                    print("eat")
                    self.currentPath = []
                    self.indexInCurrentPath = 0
                    self.pos = newPos
                    i.die(_map)
                    self.energy += i.energy
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
        #todo add check if organism can mate before making the move
        self.age += self.growthRate
        if self.age > 100:
            _map = self.die(_map)
            return _map
        if self.wait:
            return _map
        self.energy -= 1
        if self.energy <= 0:
            _map = self.die(_map)
            return _map
        objInVision = []
        for i in _map:
            if Vector.Distance(self.pos, i.pos) <= self.vision and i.pos is not self.pos:
                objInVision.append(i)
        if self.currentPath:
            _map = self.go(objInVision, _map)
            return _map
        else:
            for j in objInVision:
                if j.species == self.species:
                    if j.gender is not self.gender and self.expectations >= j.attractiveness and j.check(self) == True:
                        j.wait = True
                        objInVision.remove(j)
                        self.currentPath = self.aStar(j.pos, objInVision)
                        break
                if j.species in self.foodEat:
                    # eat
                    objInVision.remove(j)
                    self.currentPath = self.aStar(j.pos, objInVision)
                    break
            else:
                path = Vector(self.pos.x, self.pos.y)
                path.x += random.randint(-self.vision, self.vision)
                diffOfX = (path.x - self.pos.x) ** 2
                diffOfY = self.vision ** 2 - diffOfX
                path.y = round(math.sqrt(math.sqrt(diffOfY) + self.pos.y))
                self.currentPath = self.aStar(path, objInVision)
                self.pathway = 1
                self.pos = self.currentPath[self.pathway]
                self.pathway += 1
                return _map
            return _map

    def check(self, other):
        if self.expectations >= other.attractiveness:
            return True
        else:
            return False


class plant(organisms):
    """

    """

    def __init__(self, pos, energy, vision, growthRate, species):
        # noinspection PyCompatibility
        super().__init__(pos, energy, growthRate, vision, species, "plant")

    def move(self, _map):
        self.age += self.growthRate
        if self.age > 100:
            _map = self.die(_map)
        return _map


# to be implimented in other script
rabbit = animal(Vector(2, 2), 100, 1, 10, 10, 10, "rabbit", ["carrot"], "M")
anotherRabbit = animal(Vector(2, 10), 100, 1, 10, 10, 10, "rabbit", ["carrot"], "F")
_map = [rabbit, anotherRabbit]
while True:
    input("")
    for j in _map:
        _map = j.move(_map)
    print(_map)
