

'''
Credits
__author__      = "Sven Hecht"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Sven Hecht"
__email__ = "info@shdev.de"
__status__ = "Production"

to get it : https://gist.github.com/mostley/3819375

Code was used to process the Vector 2 Math required in the simulation, which I was extremely lazy to calculate. Works like a charm.

Edited it to suit my needs eg. change distance measurement from euclidean taxicab distance
'''
from math import *


class Vector:
    def __init__(self, x=0, y=0):
        self.x = 0
        self.y = 0
        if isinstance(x, tuple) or isinstance(x, list):
            y = x[1]
            x = x[0]
        elif isinstance(x, Vector):
            y = x.y
            x = x.x

        self.set(x, y)

    @staticmethod
    def Distance(self,other):
        return sqrt(pow(self.x-other.x,2)+pow(self.y-other.y,2))

    @staticmethod
    def angle(v1, v2):
        return acos(v1.dotproduct(v2) / (v1.getLength() * v2.getLength()))

    @staticmethod
    def angleDeg(v1, v2):
        return Vector.angle(v1, v2) * 180.0 / pi

    def set(self, x, y):
        self.x = x
        self.y = y

    def toArr(self):
        return [self.x, self.y]

    def toInt(self):
        return Vector(int(self.x), int(self.y))

    def toIntArr(self):
        return self.toInt().toArr()

    def getNormalized(self):
        if self.getLength() != 0:
            return self / self.getLength()
        else:
            return Vector(0, 0)

    def dotproduct(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, tuple) or isinstance(other, list):
            return self.x * other[0] + self.y * other[1]
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x + other[0], self.y + other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        if isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x - other[0], self.y - other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x - other, self.y - other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Vector):
            return Vector(other.x - self.x, other.y - self.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(other[0] - self.x, other[1] - self.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(other - self.x, other - self.y)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x * other[0], self.y * other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __div__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(self.x / other[0], self.y / other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.x / other, self.y / other)
        else:
            return NotImplemented

    def __rdiv__(self, other):
        if isinstance(other, Vector):
            return Vector(other.x / self.x, other.y / self.y)
        elif isinstance(other, tuple) or isinstance(other, list):
            return Vector(other[0] / self.x, other[1] / self.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(other / self.x, other / self.y)
        else:
            return NotImplemented

    def __pow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x ** other, self.y ** other)
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
            return self
        else:
            return NotImplemented

    def __isub__(self, other):
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x -= other[0]
            self.y -= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
            return self
        else:
            return NotImplemented

    def __imul__(self, other):
        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x *= other[0]
            self.y *= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            return self
        else:
            return NotImplemented

    def __idiv__(self, other):
        if isinstance(other, Vector):
            self.x /= other.x
            self.y /= other.y
            return self
        elif isinstance(other, tuple) or isinstance(other, list):
            self.x /= other[0]
            self.y /= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
            return self
        else:
            return NotImplemented

    def __ipow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x **= other
            self.y **= other
            return self
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Vector):
            return self.x != other.x or self.y != other.y
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Vector):
            return self.getLength() > other.getLength()
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Vector):
            return self.getLength() >= other.getLength()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Vector):
            return self.getLength() < other.getLength()
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Vector):
            return self.getLength() <= other.getLength()
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __len__(self):
        return int(sqrt(self.x ** 2 + self.y ** 2))

    def getLength(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __getitem__(self, key):
        if key == "x" or key == "X" or key == 0 or key == "0":
            return self.x
        elif key == "y" or key == "Y" or key == 1 or key == "1":
            return self.y

    def __repr__(self):
        return "[x:{0},y:{1}]".format(self.x,self.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)
