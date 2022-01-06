import json
import math

from DiGraph import DiGraph
from Location import Location



def get_pokemon_objects(json_string, graph):
    pokemons_list = []
    json_dict = json.loads(json_string)

    ID = 0
    for pokemon in json_dict['Pokemons']:
        pokemon_obj = Pokemon(pokemon, ID, graph)
        pokemons_list.append(pokemon_obj)
        ID += 1
    return pokemons_list


class Pokemon:

    def __init__(self, pokemon_dict, id, graph: DiGraph):
        self.id = id

        self.value = pokemon_dict['Pokemon']['value']
        self.type = pokemon_dict['Pokemon']['type']
        loc = pokemon_dict['Pokemon']["pos"].split(',')
        self.pos = Location(float(loc[0]), float(loc[1]), float(loc[2]))
        self.node = self.getNode(graph)
        if self.node is None:
            self.edge = self.getEdge(graph)
        else:
            self.edge = None

    def getEdge(self, graph):
        for key, edge in graph.Edges.items():
            edge_str = self.is_on_edge(edge, graph, self.type)
            if edge_str:
                return key

        return None

    def getNode(self, graph):
        for ID, node in graph.Nodes.items():
            if (node.pos.x == self.pos.x) and (node.pos.y == self.pos.y):
                return ID
        return None

    def is_on_edge(self, edge, graph: DiGraph, direction):
        if (edge.src < edge.dest and direction < 0) or (edge.src > edge.dest and direction > 0):
            return False

        dstNode = graph.Nodes.get(edge.dest)
        srcNode = graph.Nodes.get(edge.src)

        m = (dstNode.pos.y - srcNode.pos.y) / (dstNode.pos.x - srcNode.pos.x)
        a = dstNode.pos.y - m * dstNode.pos.x

        if math.isclose(self.pos.x * m + a, self.pos.y):
            return True
        else:
            return False
