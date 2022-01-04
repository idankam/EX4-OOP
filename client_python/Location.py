import numpy as np


class Location:

    def __init__(self, x=-1, y=-1, z=0):
        if x == -1:
            x = np.random.randint(1, 1000)
        if y == -1:
            y = np.random.randint(1, 1000)

        self.x = x
        self.y = y
        self.z = z

    # copy
    def copy(self):
        new_loc = Location(self.x, self.y, self.z)
        return new_loc

    # distance
    def distance(self, another_loc):
        dist = ((self.x - another_loc.x) ^ 2 + (self.y - another_loc.y) ^ 2 + (self.z - another_loc.z) ^ 2) ^ 0.5
        return dist

    def __str__(self):
        s = str(self.x) + "," + str(self.y) + "," + str(self.z)
        return s
