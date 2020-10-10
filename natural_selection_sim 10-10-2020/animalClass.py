import time
from abc import ABC, abstractmethod
from vectorMath import Vector
import sys
import random
import math


class Node():
    def __init__(self, v, f):
        self.v = v
        self.f = f

    def __repr__(self):
        return f"{self.v},{self.f}"


class animalClass(ABC):
    def __init__(self, pos, stamina, memorySize, vision):
        self.pos = pos
        self.currentPath = []
        self.pathway = 0
        self.stamina = stamina
        self.memorySize = memorySize
        self.memory = []
        self.vision = vision

    def aStar(self, end, obstacle):
        start = Node(self.pos, 0)
        open = [start]
        close = []
        previousOptions = [start]
        total = 0
        while True:
            minVal, index = sys.maxsize, 0
            for e, i in enumerate(previousOptions):
                if i.f < minVal:
                    minVal = i.f
                    index = e
            q = previousOptions[index]
            newLocations = [q.v + Vector(1, 0), q.v + Vector(0, 1),
                            q.v + Vector(0, -1), q.v + Vector(-1, 0), Vector(2, 2)]
            newLocations = [Node(i, 0) for i in newLocations]
            previousOptions.clear()
            for i in newLocations:
                if (i.v == end):
                    close.append(q)
                    close.append(Node(end, 0))
                    result = []
                    for i in close:
                        result.append(i.v)
                    return result
                shouldSkip = False
                for j in open:
                    if j.v == i.v:
                        shouldSkip = True
                for z in close:
                    if z.v == i.v:
                        shouldSkip = True
                for k in obstacle:
                    if k == i.v:
                        shouldSkip = True
                if shouldSkip:
                    continue
                else:
                    i.f = Vector.Distance(i.v, end) + Vector.Distance(i.v, start.v)
                    open.append(i)
                    previousOptions.append(i)
            close.append(q)
            open.remove(q)
            total += 1
            for i in open:
                if i.v == q.v:
                    raise Exception("did not pop")
            if (total == 10000):
                raise Exception("couldnt find path")

    @abstractmethod
    def move(self, map):
        pass

    def __repr__(self):
        return self.type + "\t" + str(self.pos) + "\t" + str(self.stamina)

    def die(self, map):
        map.remove(self)
        return map

    def eat(self, food, map):
        self.memory.remove((food, Vector.Distance(food.pos, self.pos)))
        self.stamina += food.energy
        map.remove(food)
        self.pos = food.pos
        self.target = None
        return map


class prey(animalClass):
    def __init__(self, pos, stamina, memorySize, vision):
        self.type = 'prey'
        super().__init__(pos, stamina, memorySize, vision)

    def getRandomPath(self, obstacle, map):
        path = Vector(self.pos.x, self.pos.y)
        path.x += random.randint(-self.vision, self.vision)
        diffOfX = (path.x - self.pos.x) ** 2
        diffOfY = self.vision ** 2 - diffOfX
        path.y = round(math.sqrt(math.sqrt(diffOfY) + self.pos.y))
        self.currentPath = self.aStar(path, obstacle)
        self.pathway = 1
        self.pos = self.currentPath[self.pathway]
        self.pathway += 1
        return map

    def move(self, map):
        # get range of all coordinates it can see
        # if plant, lock on it
        # no path,no plant, get random location in vision
        # if path, go to path
        self.stamina -= 1
        if self.stamina < 1:
            self.die(map)
        self.memory = []
        obstacle = []
        for i in map:
            if i.pos != self.pos and Vector.Distance(i.pos, self.pos) < self.vision and i.type == 'plant':
                self.memory.append((i, Vector.Distance(i.pos, self.pos)))
            if i.pos != self.pos and Vector.Distance(i.pos, self.pos) and i.type != 'plant':
                obstacle.append(i)
        if self.memory:
            while len(self.memory) > self.memorySize:
                self.memory.pop(0)
            lowest, index = sys.maxsize, 0
            for e, (_, i) in enumerate(self.memory):
                if i < lowest:
                    lowest = i
                    index = e
            if self.aStar(self.memory[index][0].pos, obstacle)[1] == self.memory[index][0].pos:
                self.eat(self.memory[index][0], map)
            else:
                self.pos = self.aStar(self.memory[index][0].pos, obstacle)[1]

        else:
            if not self.currentPath:
                self.getRandomPath(obstacle, map)
            else:
                if self.pathway != len(self.currentPath):
                    self.pos = self.currentPath[self.pathway]
                    self.pathway += 1
                else:
                    self.currentPath.clear()

        return map
