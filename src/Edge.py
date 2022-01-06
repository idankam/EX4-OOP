# from client_python.DiGraph import DiGraph
from src.Location import Location


class Edge:

    def __init__(self, src, w, dest):
        self.src = src
        self.dest = dest
        self.weight = w

    def __repr__(self):
        s = "src: " + str(self.src) + ", dest: " + str(self.dest) + ", w: " + str(self.weight)
        return s


