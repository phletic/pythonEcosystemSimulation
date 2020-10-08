import time
from abc import ABC, abstractmethod
from vectorMath import Vector
import sys
import random

'''
This progam will store all the animal classes.
I hope I will be able to allow the user to create his own organisms with custom behavious AKA edit the program through a UI
'''
#This Node is for the a* algorithm. THe Repr method is pretty useless as I wouldn't print it but still I guess no harm keeping...
class Node():
    def __init__(self, v, f):
        self.v = v
        self.f = f

    def __repr__(self):
        return f"{self.v},{self.f}"

#animal class. the parent
class animalClass(ABC):
    def __init__(self, pos, stamina):
        self.pos = pos
        self.currentPath = []
        self.pathway = 0
        self.type = ""
        self.stamina = stamina

    #That one annoying a star program
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

    def die(self,map):
        map.remove(self)
        return map
#Prey class, the child. But soon I want to make it that there will be animals branching out from this class
class prey(animalClass):
    def start(self):
        self.type = "prey"
    # gets shortest path
    def calculate(self, map, types, locations):
        shortestDistance, plant = sys.maxsize, 0
        for e, i in enumerate(map):
            if i.type == 'plant':
                distance = Vector.Distance(self.pos, i.pos)
                if distance < shortestDistance:
                    shortestDistance = distance
                    plant = e
        goal = map[plant].pos
        if "plant" not in types:
            goal = Vector(random.randint(0, 10), random.randint(0, 10))
        self.currentPath = self.aStar(goal, obstacle=locations)
        self.pathway = 0
        self.pos = self.currentPath[self.pathway]
        self.pathway += 1
        return map

    def move(self, map):
        if(self.stamina < 1):
            self.die(map)
        self.stamina -= 1
        locations = [i.pos for i in map]
        types = [i.type for i in map]
        if not self.currentPath or self.pathway == len(self.currentPath):
            map = self.calculate(map, types, locations)
            return map
        else:
            #when there is no paths
            if self.currentPath[self.pathway] not in locations:
                self.pos = self.currentPath[self.pathway]
                self.pathway += 1
                return map
            #when there is food
            elif self.currentPath[self.pathway] in locations:
                eaten = False
                for i in map:
                    #num num num
                    if i.type == "plant" and self.currentPath[self.pathway] == i.pos:
                        self.pos = i.pos
                        self.stamina += i.energy
                        map.remove(i)
                        self.pathway += 1
                        eaten = True
                if(eaten):
                    return map
                else:
                    #there is an obstruction
                    map = self.calculate(map, types, locations)
                    return map
                
#TODO predator 

