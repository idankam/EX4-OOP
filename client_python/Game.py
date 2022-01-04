import sys

import numpy
from client_python.Pokemon import *
from client_python.GraphAlgo import GraphAlgo
from client_python.Pokemon import get_pokemon_objects
from client_python.Agent import get_agents_objects
from client_python.client import Client

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'


class Game:

    def __init__(self):

        self.client = Client()
        self.client.start_connection(HOST, PORT)

        self.graphAlgo = GraphAlgo()
        graph_json = self.client.get_graph()
        self.graphAlgo.load_from_json(graph_json)

        self.pokemons_list = get_pokemon_objects(self.client.get_pokemons(), self.graphAlgo.get_graph())

        i = 0
        s = "true"
        while s == "true":
            send = '{\"id\":' + str(i) + '}'
            s = self.client.add_agent(send)
            i += 1

        self.client.start()
        # print("here!")
        # print(self.client.get_agents())
        self.agents_list = get_agents_objects(self.client.get_agents())
        # self.add_agents_to_game()

    def update_game_info(self):
        self.pokemons_list = get_pokemon_objects(self.client.get_pokemons(), self.graphAlgo.get_graph())
        self.agents_list = get_agents_objects(self.client.get_agents())

    def update_dest_for_agents(self):
        flag = False
        self.sort_pokemons_by_value()
        for pokemon in self.pokemons_list:
            best_agent = None
            best_agent_id = -1
            best_agent_distance = sys.maxsize
            best_agent_next_node = -1
            pokemon_src = pokemon.node
            if pokemon_src is None:
                pokemon_src = int(pokemon.edge.split(',')[0])
                pokemon_dest = int(pokemon.edge.split(',')[1])

            for agent in self.agents_list:
                if agent.dest == -1:

                    if agent.src == pokemon_src:
                        best_agent = agent
                        best_agent_id = agent.id
                        best_agent_next_node = pokemon_dest
                        break

                    distance, nodes_list = self.graphAlgo.shortest_path(agent.src, pokemon_src)
                    if distance < best_agent_distance:
                        best_agent = agent
                        best_agent_id = agent.id
                        best_agent_distance = distance
                        best_agent_next_node = nodes_list[0]

            if best_agent_id != -1:
                flag = True
                self.agents_list.remove(best_agent)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(best_agent_id) + ', "next_node_id":' + str(best_agent_next_node) + '}')
        if flag:
            self.client.move()

    def sort_pokemons_by_value(self):
        self.pokemons_list.sort(key=lambda x: x.value, reverse=True)

    def print_status(self):
        ttl = self.client.time_to_end()
        print(ttl, self.client.get_info())

    # def add_agents_to_game(self):
    #     # complete!
    #     self.client.add_agent("{\"id\":0}")
