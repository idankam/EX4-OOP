import sys
import numpy
from src.GraphAlgo import GraphAlgo
from src.Pokemon import get_pokemon_objects
from src.Agent import get_agents_objects
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
        self.add_agents_to_game()
        self.agents_list = get_agents_objects(self.client.get_agents())
        self.client.start()

    def update_game_info(self):
        self.pokemons_list = get_pokemon_objects(self.client.get_pokemons(), self.graphAlgo.get_graph())
        self.agents_list = get_agents_objects(self.client.get_agents())

    def add_agents_to_game(self):
        s = "true"
        ids = list(self.graphAlgo.get_graph().Nodes.keys())
        center, dist = self.graphAlgo.centerPoint()
        while s == "true":
            send = '{\"id\":' + str(center) + '}'
            s = self.client.add_agent(send)
            rand = numpy.random.randint(0, len(ids) - 1)
            center = ids[rand]

    def update_dest_value_per_second(self):
        if self.pokemons_list is None:
            self.client.move()
        else:
            time_flag = True

            while (len(self.pokemons_list) > 0) and (len(self.agents_list) > 0) and time_flag:

                best_agent = None
                best_agent_id = -1
                best_agent_value_per_second = -sys.maxsize - 1
                best_agent_next_node = -1
                best_pokemon = None

                for pokemon in self.pokemons_list:
                    for agent in self.agents_list:

                        pokemon_src = pokemon.node
                        pokemon_dest = pokemon_src
                        if pokemon_src is None:
                            pokemon_src = int(pokemon.edge.split(',')[0])
                            pokemon_dest = int(pokemon.edge.split(',')[1])

                        distance, nodes_list = self.graphAlgo.shortest_path(agent.src, pokemon_src)

                        if distance == 0:
                            distance = self.graphAlgo.get_graph().Edges.get(
                                str(pokemon_src) + "," + str(pokemon_dest)).weight
                            next_node = pokemon_dest
                        else:
                            next_node = nodes_list[1]

                        value_per_second = float(pokemon.value) / (distance / agent.speed)

                        if best_agent_value_per_second < value_per_second:
                            best_agent = agent
                            best_agent_id = agent.id
                            best_agent_value_per_second = value_per_second
                            best_agent_next_node = next_node
                            best_pokemon = pokemon
                self.pokemons_list.remove(best_pokemon)
                self.agents_list.remove(best_agent)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(best_agent_id) + ', "next_node_id":' + str(best_agent_next_node) + '}')
            self.client.move()

    # def IDAN_update_dest_for_agents_by_biggest_value(self):
    #
    #     if self.pokemons_list is None:
    #         self.client.move()
    #     else:
    #         flag = False
    #         self.sort_pokemons_by_value()
    #         for pokemon in self.pokemons_list:
    #             best_agent = None
    #             best_agent_id = -1
    #             best_agent_distance = sys.maxsize
    #             best_agent_next_node = -1
    #             pokemon_src = pokemon.node
    #             if pokemon_src is None:
    #                 pokemon_src = int(pokemon.edge.split(',')[0])
    #                 pokemon_dest = int(pokemon.edge.split(',')[1])
    #
    #             for agent in self.agents_list:
    #                 if agent.dest == -1:
    #
    #                     if agent.src == pokemon_src:
    #                         best_agent = agent
    #                         best_agent_id = agent.id
    #                         best_agent_next_node = pokemon_dest
    #                         break
    #
    #                     distance, nodes_list = self.graphAlgo.shortest_path(agent.src, pokemon_src)
    #                     if distance < best_agent_distance:
    #                         best_agent = agent
    #                         best_agent_id = agent.id
    #                         best_agent_distance = distance
    #                         best_agent_next_node = nodes_list[1]
    #
    #             if best_agent_id != -1:
    #                 flag = True
    #                 print((best_agent, best_agent_id, best_agent_distance, best_agent_next_node))
    #                 self.agents_list.remove(best_agent)
    #                 self.client.choose_next_edge(
    #                     '{"agent_id":' + str(best_agent_id) + ', "next_node_id":' + str(best_agent_next_node) + '}')
    #
    #         self.client.move()

    # def update_dest_for_agents_minimal_path(self):
    #     if self.pokemons_list is None:
    #         self.client.move()
    #     else:
    #         print((1, self.pokemons_list, self.agents_list))
    #         agents_to_remove = []
    #         pokemon_to_remove = []
    #         for pokemon in self.pokemons_list:
    #             pokemon_src = pokemon.node
    #             pokemon_dest = pokemon_src
    #             if pokemon_src is None:
    #                 pokemon_src = int(pokemon.edge.split(',')[0])
    #                 pokemon_dest = int(pokemon.edge.split(',')[1])
    #             for agent in self.agents_list:
    #                 if agent.dest == -1:
    #                     if agent.src == pokemon_src:
    #                         agents_to_remove.append(agent)
    #                         if pokemon not in pokemon_to_remove:
    #                             pokemon_to_remove.append(pokemon)
    #                         self.client.choose_next_edge(
    #                             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
    #                                 pokemon_dest) + '}')
    #
    #             for agent in agents_to_remove:
    #                 self.agents_list.remove(agent)
    #             agents_to_remove = []
    #         for pokemon in pokemon_to_remove:
    #             self.pokemons_list.remove(pokemon)
    #
    #         print((2, self.pokemons_list, self.agents_list))
    #         while (len(self.pokemons_list) > 0) and (len(self.agents_list) > 0):
    #             print(("len", len(self.pokemons_list), len(self.agents_list)))
    #             self.sort_pokemons_by_value()
    #             best_agent = None
    #             best_agent_id = -1
    #             best_agent_distance = sys.maxsize
    #             best_agent_next_node = -1
    #             pokemon_to_remove = None
    #
    #             i = 0
    #             for pokemon in self.pokemons_list:
    #                 print(("i", i))
    #                 pokemon_src = pokemon.node
    #                 pokemon_dest = pokemon_src  # just in case
    #                 if pokemon_src is None:
    #                     pokemon_src = int(pokemon.edge.split(',')[0])
    #                     pokemon_dest = int(pokemon.edge.split(',')[1])
    #
    #                 j = 0
    #                 for agent in self.agents_list:
    #                     print(("j", j))
    #                     if agent.dest == -1:
    #
    #                         if agent.src == pokemon_src:
    #                             best_agent = agent
    #                             best_agent_id = agent.id
    #                             best_agent_distance = 0
    #                             best_agent_next_node = pokemon_dest
    #                             pokemon_to_remove = pokemon
    #                             break
    #
    #                         distance, nodes_list = self.graphAlgo.shortest_path(agent.src, pokemon_src)
    #                         if distance < best_agent_distance:
    #                             best_agent = agent
    #                             best_agent_id = agent.id
    #                             best_agent_distance = distance
    #                             best_agent_next_node = nodes_list[1]
    #                             pokemon_to_remove = pokemon
    #
    #                 if best_agent_id != -1:
    #                     print((best_agent, best_agent_id, best_agent_distance, best_agent_next_node))
    #                     self.agents_list.remove(best_agent)
    #                     self.pokemons_list.remove(pokemon_to_remove)
    #                     self.client.choose_next_edge(
    #                         '{"agent_id":' + str(best_agent_id) + ', "next_node_id":' + str(best_agent_next_node) + '}')
    #             print(3, (self.pokemons_list, self.agents_list))
    #         self.client.move()

    # def make_move(self):

    # def update_dest_for_agents_by_tsp(self):
    #
    #     if self.pokemons_list is None:
    #         self.client.move()
    #     else:
    #         self.sort_pokemons_by_value()
    #
    #         cities = []
    #         for pokemon in self.pokemons_list:
    #             pokemon_src = pokemon.node
    #             if pokemon_src is not None:
    #                 cities.append(pokemon_src)
    #             else:
    #                 pokemon_src = int(pokemon.edge.split(',')[0])
    #                 pokemon_dest = int(pokemon.edge.split(',')[1])
    #                 cities.append(pokemon_src)
    #                 cities.append(pokemon_dest)
    #
    #         agents_to_remove = []
    #         for pokemon in self.pokemons_list:
    #             pokemon_src = pokemon.node
    #             if pokemon_src is None:
    #                 pokemon_src = int(pokemon.edge.split(',')[0])
    #                 pokemon_dest = int(pokemon.edge.split(',')[1])
    #             for agent in self.agents_list:
    #                 if agent.dest == -1:
    #                     if agent.src == pokemon_src:
    #                         agents_to_remove.append(agent)
    #                         self.client.choose_next_edge(
    #                             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
    #                                 pokemon_dest) + '}')
    #
    #             for agent in agents_to_remove:
    #                 self.agents_list.remove(agent)
    #             agents_to_remove = []
    #
    #         for agent in self.agents_list:
    #             if agent.dest == -1:
    #                 print(cities)
    #                 if cities[0] != agent.src:
    #                     cities = [agent.src] + cities
    #                     print(cities)
    #
    #                 nodes_list, distance = self.graphAlgo.TSP(cities.copy())
    #                 print("nodes_list:")
    #                 print(nodes_list)
    #                 self.client.choose_next_edge(
    #                     '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(nodes_list[1]) + '}')
    #
    #         self.client.move()
    #
    # def powerset(self, iterable):
    #     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    #     s = list(iterable)
    #     return chain.from_iterable(combinations(s, r) for r in range(1, 5))
    #
    # def update_dest_for_agents_by_tsp_test(self):
    #
    #     if self.pokemons_list is not None:
    #
    #         #  check!
    #         # self.sort_pokemons_by_value()
    #
    #         # agents_to_remove = []
    #         # for pokemon in self.pokemons_list:
    #         #     pokemon_src = pokemon.node
    #         #     if pokemon_src is None:
    #         #         pokemon_src = int(pokemon.edge.split(',')[0])
    #         #         pokemon_dest = int(pokemon.edge.split(',')[1])
    #         #     for agent in self.agents_list:
    #         #         if agent.dest == -1:
    #         #             if agent.src == pokemon_src:
    #         #                 agents_to_remove.append(agent)
    #         #                 self.client.choose_next_edge(
    #         #                     '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
    #         #                         pokemon_dest) + '}')
    #
    #         # for agent in agents_to_remove:
    #         #     self.agents_list.remove(agent)
    #         pokemon_to_remove = []
    #         agents_to_remove = []
    #         for agent in self.agents_list:
    #             if agent.id in self.agents_waze.keys() and agent.dest == -1:
    #                 if len(self.agents_waze[agent.id]) > 1:
    #                     self.agents_waze[agent.id].remove(agent.src)
    #                     self.client.choose_next_edge(
    #                         '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(
    #                             self.agents_waze[agent.id][0]) + '}')
    #                     agents_to_remove.append(agent)
    #
    #                     for pokemon in self.pokemons_list:
    #                         if pokemon.pos.__str__() in self.pokemon_allocated[agent.id]:
    #                             pokemon_to_remove.append(pokemon)
    #                             print("yes!!")
    #                 else:
    #                     del self.agents_waze[agent.id]
    #                     del self.pokemon_allocated[agent.id]
    #
    #         for agent in agents_to_remove:
    #             self.agents_list.remove(agent)
    #         for pok in pokemon_to_remove:
    #             self.pokemons_list.remove(pok)
    #
    #         for agent in self.agents_list:
    #             if agent.dest == -1 and len(self.pokemons_list) > 0:
    #
    #                 nodes_cities, best_pokemons = self.tsp_best(agent)
    #
    #                 self.agents_waze[agent.id] = nodes_cities[1:]
    #                 # print("nodes_list:")
    #                 # print(nodes_list)
    #                 self.pokemon_allocated[agent.id] = []
    #                 for pok in best_pokemons:
    #                     self.pokemons_list.remove(pok)
    #                     self.pokemon_allocated[agent.id].append(pok.pos.__str__())
    #
    #                 self.client.choose_next_edge(
    #                     '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(nodes_cities[1]) + '}')
    #
    #     self.client.move()
    #
    # def tsp_best(self, agent):
    #
    #     best_value_per_seconds = -1
    #     best_pokemons = None
    #     best_cities = None
    #     print("agent:" + str(agent.id))
    #     for pokemons in self.powerset(self.pokemons_list):
    #
    #         cities = []
    #         pokemons_value = 0
    #         for pokemon in pokemons:
    #
    #             pokemons_value += pokemon.value
    #             pokemon_src = pokemon.node
    #             if pokemon_src is not None:
    #                 cities.append(pokemon_src)
    #             else:
    #                 pokemon_src = int(pokemon.edge.split(',')[0])
    #                 pokemon_dest = int(pokemon.edge.split(',')[1])
    #                 cities.append(pokemon_src)
    #                 cities.append(pokemon_dest)
    #             # print(pokemon_src)
    #         if cities[0] != agent.src:
    #             cities = [agent.src] + cities
    #
    #         # print("cities:" + str(cities))
    #
    #         nodes_list, distance = self.graphAlgo.TSP(cities.copy())
    #         value_per_seconds = pokemons_value / (distance / agent.speed)
    #         if value_per_seconds > best_value_per_seconds:
    #             best_value_per_seconds = value_per_seconds
    #             best_cities = nodes_list
    #             best_pokemons = pokemons
    #
    #         # print("value: {}, dist: {}, speed: {}, value_per: {}".format(pokemons_value, distance, agent.speed, value_per_seconds))
    #
    #     print("BEST! value_per: {}".format(value_per_seconds))
    #     for p in best_pokemons:
    #         print(p.edge.split(',')[0])
    #     return best_cities, best_pokemons
    #
    # def sort_pokemons_by_value(self):
    #     self.pokemons_list.sort(key=lambda x: x.value, reverse=True)

    # def print_status(self):
    #     ttl = self.client.time_to_end()
    #     print(ttl, self.client.get_info())

    # def add_agents_to_game(self):
    #     # complete!
    #     self.client.add_agent("{\"id\":0}")

    # def GABI_update_dest_for_agents(self):
    #     usedPokemons = []
    #     dictNextDest = {}
    #
    #     for agent in self.agents_list:
    #         if agent.dest == -1:
    #             nextdest, minimumPokemonId = self.findClosestPokemon(agent, usedPokemons)
    #             usedPokemons.append(minimumPokemonId)
    #             dictNextDest[agent.id] = nextdest
    #
    #     print(dictNextDest)
    #
    #     for key, next_node in dictNextDest.items():
    #         # next_node = dictNextDest.get(key)
    #         self.client.choose_next_edge(
    #             '{"agent_id":' + str(key) + ', "next_node_id":' + str(next_node) + '}')
    #     ttl = self.client.time_to_end()
    #     print(ttl, self.client.get_info())
    #     self.client.move()
    #
    #     # return dictNextDest

    # def findClosestPokemon(self, agent, usedPokemons):
    #     min = sys.maxsize
    #     for pokemon in self.pokemons_list:
    #         if pokemon.id not in usedPokemons:
    #             pokemonSrcStr = pokemon.edge.split(',')
    #             pokemonSrc = int(pokemonSrcStr[0])
    #             pokemonDst = int(pokemonSrcStr[1])
    #
    #             distance, ls = self.graphAlgo.shortest_path(agent.src, pokemonSrc)
    #
    #             if distance == 0:
    #                 return pokemonDst, pokemon.id
    #
    #             if distance < min:
    #                 nextdest = ls[1]
    #                 minimumPokemonId = pokemon.id
    #
    #     return nextdest, minimumPokemonId
