from animalClass import prey
from food import plant
from vectorMath import Vector
import time

'''
driver program. 
'''
'''
prey(stamina, memorysize,vision)
'''
map = [prey(Vector(0, 5), 10,10,10),plant(Vector(2, 0), 5),plant(Vector(1, 0), 5)]
# this starts up the organisms. For now, it only assigns its type (str). But I think it will be very useful later when the program gets moew advanced

if __name__ == '__main__':
    while True:
        int = input("")
        for e, i in enumerate(map):
            if i.type == 'prey':
                map = map[e].move(map)


        print(map)
