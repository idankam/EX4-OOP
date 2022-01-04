import numpy

from client_python.client import Client


class Game:

    def __init__(self, graphAlgo, pokemons_list, agents_list, client):
        self.client = client
        self.agents_list = agents_list
        self.pokemons_list = pokemons_list
        self.graphAlgo = graphAlgo

    def update_dest_for_agents(self):

        self.sort_pokemons_by_value()
        for pokemon in self.pokemons_list:
            best_agent_id = -1
            best_agent_distance = numpy.Infinity

        for agent in self.agents_list:
            if agent.dest == -1:
                self.graphAlgo.shortest_path(agent.src, )