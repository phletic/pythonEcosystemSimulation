import time
'''
code by Chavez Chen
created on 7/10/2020 
This program aims to test the A* program before starting on the actual simulation project
'''
from vectorMath import *
import sys
class Node():
    def __init__(self,v,f):
        self.v = v
        self.f = f
    def __repr__(self):
        return f"{self.v},{self.f}"

start = Node(Vector(-2,2),0)
end = Vector(2,10)
def aStar():
    open=[start]
    close=[]
    previousOptions=[start]
    total = 0
    while True:
        print(close,"\n",open,"\n")
        minVal,index = sys.maxsize,0
        for e,i in enumerate(previousOptions):
            if i.f<minVal:
                minVal = i.f
                index = e
        q = previousOptions[index]
        newLocations = [q.v+Vector(1,0),q.v+Vector(0,1),
                        q.v+Vector(0,-1),q.v+Vector(-1,0)]
        newLocations = [Node(i,0) for i in newLocations]
        previousOptions.clear()
        for i in newLocations:
            if(i.v == end):
                close.append(q)
                close.append(Node(end,0))
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
            if shouldSkip:
                continue
            else:
                i.f = Vector.Distance(i.v,end)+Vector.Distance(i.v,start.v)
                open.append(i)
                previousOptions.append(i)
        close.append(q)
        open.remove(q)
        total += 1
        for i in open:
            if i.v == q.v:
                raise Exception("did not pop")
        if(total == 10000):
            raise Exception("couldnt find path")

print(aStar())