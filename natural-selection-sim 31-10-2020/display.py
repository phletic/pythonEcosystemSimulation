from commandCode import *
from sys import argv

syntax = {
    "createAnimal": createAnimal,
    "createMap": createMap,
    "addAnimal": addAnimal,
    "addPlant": addPlant,
    "createPlant": createPlant,
    "deleteAnimal": deleteAnimal,
    "deletePlant": deletePlant,
    "deleteMap": deleteMap,
    "printMap": printMap,
    "run": run

}
command = argv[1:]
object = syntax[command[0]](*command[1:])
print("running {0}".format(".".join(command)))
object.run()