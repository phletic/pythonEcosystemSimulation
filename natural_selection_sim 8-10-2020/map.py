from animalClass import prey
from food import plant
from vectorMath import Vector
import time

map = [prey(Vector(0, 0), 10), prey(Vector(1, 0), 10), plant(Vector(2, 0), 5)]
for i in map:
    i.start()
if __name__ == '__main__':
    while True:
        int = input("")
        for e, i in enumerate(map):
            if i.type == 'prey':
                map = map[e].move(map)
        print(map)
