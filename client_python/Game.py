import sys
from operator import length_hint

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
        self.agents_list = get_agents_objects(self.client.get_agents())
        self.client.start()
        # print("here!")
        # print(self.client.get_agents())
        # self.add_agents_to_game()

    def update_game_info(self):
        self.pokemons_list = get_pokemon_objects(self.client.get_pokemons(), self.graphAlgo.get_graph())
        self.agents_list = get_agents_objects(self.client.get_agents())

    def update_dest_for_agents_by_biggest_value(self):

        if self.pokemons_list is None:
            self.client.move()
        else:
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
                            best_agent_next_node = nodes_list[1]

                if best_agent_id != -1:
                    flag = True
                    print((best_agent, best_agent_id, best_agent_distance, best_agent_next_node))
                    self.agents_list.remove(best_agent)
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(best_agent_id) + ', "next_node_id":' + str(best_agent_next_node) + '}')

            self.client.move()

    def update_dest_for_agents_minimal_path(self):

        if self.pokemons_list is None:
            self.client.move()
        else:

            print((1, self.pokemons_list, self.agents_list))
            agents_to_remove = []
            pokemon_to_remove = []
            for pokemon in self.pokemons_list:
                pokemon_src = pokemon.node
                pokemon_dest = pokemon_src
                if pokemon_src is None:
                    pokemon_src = int(pokemon.edge.split(',')[0])
                    pokemon_dest = int(pokemon.edge.split(',')[1])
                for agent in self.agents_list:
                    if agent.dest == -1:
                        if agent.src == pokemon_src:
                            agents_to_remove.append(agent)
                            if pokemon not in pokemon_to_remove:
                                pokemon_to_remove.append(pokemon)
                            self.client.choose_next_edge(
                                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
                                    pokemon_dest) + '}')

                for agent in agents_to_remove:
                    self.agents_list.remove(agent)
                agents_to_remove = []

            for pokemon in pokemon_to_remove:
                self.pokemons_list.remove(pokemon)

            print((2, self.pokemons_list, self.agents_list))
            while (len(self.pokemons_list) > 0) and (len(self.agents_list) > 0):
                print(("len", len(self.pokemons_list), len(self.agents_list)))
                self.sort_pokemons_by_value()
                best_agent = None
                best_agent_id = -1
                best_agent_distance = sys.maxsize
                best_agent_next_node = -1
                pokemon_to_remove = None

                i = 0
                for pokemon in self.pokemons_list:
                    print(("i", i))
                    pokemon_src = pokemon.node
                    pokemon_dest = pokemon_src  # just in case
                    if pokemon_src is None:
                        pokemon_src = int(pokemon.edge.split(',')[0])
                        pokemon_dest = int(pokemon.edge.split(',')[1])

                    j = 0
                    for agent in self.agents_list:
                        print(("j", j))
                        if agent.dest == -1:

                            if agent.src == pokemon_src:
                                best_agent = agent
                                best_agent_id = agent.id
                                best_agent_distance = 0
                                best_agent_next_node = pokemon_dest
                                pokemon_to_remove = pokemon
                                break

                            distance, nodes_list = self.graphAlgo.shortest_path(agent.src, pokemon_src)
                            if distance < best_agent_distance:
                                best_agent = agent
                                best_agent_id = agent.id
                                best_agent_distance = distance
                                best_agent_next_node = nodes_list[1]
                                pokemon_to_remove = pokemon

                    if best_agent_id != -1:
                        print((best_agent, best_agent_id, best_agent_distance, best_agent_next_node))
                        self.agents_list.remove(best_agent)
                        self.pokemons_list.remove(pokemon_to_remove)
                        self.client.choose_next_edge(
                            '{"agent_id":' + str(best_agent_id) + ', "next_node_id":' + str(best_agent_next_node) + '}')
                print(3, (self.pokemons_list, self.agents_list))
            self.client.move()

    def update_dest_for_agents_by_tsp(self):

        if self.pokemons_list is None:
            self.client.move()
        else:
            self.sort_pokemons_by_value()

            cities = []
            for pokemon in self.pokemons_list:
                pokemon_src = pokemon.node
                if pokemon_src is not None:
                    cities.append(pokemon_src)
                else:
                    pokemon_src = int(pokemon.edge.split(',')[0])
                    pokemon_dest = int(pokemon.edge.split(',')[1])
                    cities.append(pokemon_src)
                    cities.append(pokemon_dest)

            agents_to_remove = []
            for pokemon in self.pokemons_list:
                pokemon_src = pokemon.node
                if pokemon_src is None:
                    pokemon_src = int(pokemon.edge.split(',')[0])
                    pokemon_dest = int(pokemon.edge.split(',')[1])
                for agent in self.agents_list:
                    if agent.dest == -1:
                        if agent.src == pokemon_src:
                            agents_to_remove.append(agent)
                            self.client.choose_next_edge(
                                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
                                    pokemon_dest) + '}')

                for agent in agents_to_remove:
                    self.agents_list.remove(agent)
                agents_to_remove = []

            for agent in self.agents_list:
                if agent.dest == -1:
                    print(cities)
                    if cities[0] != agent.src:
                        cities = [agent.src] + cities
                        print(cities)

                    nodes_list, distance = self.graphAlgo.TSP(cities)
                    print("nodes_list:")
                    print(nodes_list)
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(nodes_list[1]) + '}')

            self.client.move()

    def sort_pokemons_by_value(self):
        self.pokemons_list.sort(key=lambda x: x.value, reverse=True)

    def print_status(self):
        ttl = self.client.time_to_end()
        print(ttl, self.client.get_info())

    # def add_agents_to_game(self):
    #     # complete!
    #     self.client.add_agent("{\"id\":0}")

    def update_dest_for_agents2(self):
        usedPokemons = []
        dictNextDest = {}
        # for pokemon in self.pokemons_list:
        #     best_agent_id = -1
        #     best_agent_distance = numpy.Infinity
        for agent in self.agents_list:
            if agent.dest == -1:
                ans = self.findClosestPokemon(agent, usedPokemons)
                usedPokemons.append(ans[1])
                dictNextDest[agent.id] = ans[1]

        for key in dictNextDest.keys():
            next_node = dictNextDest.get(key)
            self.client.choose_next_edge(
                '{"agent_id":' + str(key) + ', "next_node_id":' + str(next_node) + '}')
        ttl = self.client.time_to_end()
        print(ttl, self.client.get_info())
        self.client.move()

        # return dictNextDest

    def findClosestPokemon(self, agent, usedPokemons):
        # dictClosestPokemon = {}
        # usedPokemons = []
        # for agent in self.agents_list:
        min = sys.maxsize
        for pokemon in self.pokemons_list:
            if pokemon.id not in usedPokemons:
                pokemonSrcStr = pokemon.edge.split(',')
                pokemonSrc = (int)(pokemonSrcStr[0])
                currDest = self.graphAlgo.shortest_path(agent.src, pokemonSrc)
                if currDest[0] < min:
                    nextdest = currDest[1][1]
                    minimumPokemonId = pokemon.id

                    # dictClosestPokemon[agent.id] = minList
                return nextdest, minimumPokemonId
