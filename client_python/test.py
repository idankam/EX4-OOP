"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import random
import subprocess
import os
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.GraphAlgo import GraphAlgo
from client_python.Pokemon import *
from client_python.Game import Game
from Location import Location

# init pygame
WIDTH, HEIGHT = 1080, 720

pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)

game = Game()


graph_json = game.client.get_graph()
graph_dict = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
# graphA = GraphAlgo()
# print(graphA.load_from_json(graph_json))
# print(graphA.get_graph())


for n in graph_dict.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph_dict.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph_dict.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph_dict.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph_dict.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now


"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while game.client.is_running() == 'true':
    try:

        pokemons = json.loads(game.client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        for p in pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=my_scale(
                float(x), x=True), y=my_scale(float(y), y=True))
        agents = json.loads(game.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for a in agents:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=my_scale(
                float(x), x=True), y=my_scale(float(y), y=True))
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        pBackRound = pygame.image.load('pokemon.png')
        pBackRound = pygame.transform.scale(pBackRound, (1080,1120))
        # refresh surface1080, 720
        screen.fill(Color(0, 0, 0))
        screen.blit(pBackRound,(0,-195))

        # draw nodes
        for n in graph_dict.Nodes:
            x = my_scale(n.pos.x, x=True)
            y = my_scale(n.pos.y, y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  radius, Color(64, 80, 174))
            gfxdraw.aacircle(screen, int(x), int(y),
                             radius, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

        # draw edges
        for e in graph_dict.Edges:
            # find the edge nodes
            src = next(n for n in graph_dict.Nodes if n.id == e.src)
            dest = next(n for n in graph_dict.Nodes if n.id == e.dest)

            # scaled positions
            src_x = my_scale(src.pos.x, x=True)
            src_y = my_scale(src.pos.y, y=True)
            dest_x = my_scale(dest.pos.x, x=True)
            dest_y = my_scale(dest.pos.y, y=True)

            # draw the line
            pygame.draw.line(screen, Color(255, 255, 51),
                             (src_x, src_y), (dest_x, dest_y))

        pokeball = pygame.image.load('pokeball.png')
        pokeball = pygame.transform.scale(pokeball, (38, 30))

        pokeTrainer = pygame.image.load('pokemon-trainer.png')
        pokeTrainer = pygame.transform.scale(pokeTrainer, (50, 40))

        # draw agents
        for agent in agents:
            # agentLoc = Location(float(agent.pos.x),float(agent.pos.y),0.0)
            # for p in pokemons:
            #     pokemonLoc = Location(float(p.pos.x), float(p.pos.y),0.0)
            #     dist =(agentLoc.distance(pokemonLoc))
            #     if dist < 50 :
            #         screen.blit(pokeball, (float(agent.pos.x) - 20, float(agent.pos.y) - 20))
            #     else:
             screen.blit(pokeTrainer, (float(agent.pos.x) - 20, float(agent.pos.y) - 20))


            #pygame.draw.circle(screen, Color(122, 61, 23),
             #                  (int(agent.pos.x), int(agent.pos.y)), 10)

        listDrawPokemons = []

        pikachu = pygame.image.load('pikachu.png')
        pikachu = pygame.transform.scale(pikachu, (43, 36))

        listDrawPokemons.append(pikachu)

        bullbasaur = pygame.image.load('bullbasaur.png')
        bullbasaur = pygame.transform.scale(bullbasaur, (43, 36))

        listDrawPokemons.append(bullbasaur)

        snorlax = pygame.image.load('snorlax.png')
        snorlax = pygame.transform.scale(snorlax, (43, 36))

        listDrawPokemons.append(snorlax)

        charmander = pygame.image.load('charmander.png')
        charmander = pygame.transform.scale(charmander, (43, 36))

        listDrawPokemons.append(charmander)

        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
        for p in pokemons:
            pokemonLoc = Location(float(p.pos.x), float(p.pos.y), 0.0)
            for agent in agents:
                agentLoc = Location(float(agent.pos.x), float(agent.pos.y), 0)
                dist = (agentLoc.distance(pokemonLoc))
                if dist < 85 and ((agent.src - agent.dest < 0 and p.type >= 0) or (agent.src - agent.dest > 0 and p.type < 0)):
                    screen.blit(pokeball, (float(p.pos.x) - 20, float(p.pos.y) - 20))
                else:
                  if p.value%4 == 0:
                    screen.blit(listDrawPokemons[0], (float(p.pos.x) - 20, float(p.pos.y) - 20))
                  elif p.value%4 == 1:
                    screen.blit(listDrawPokemons[1], (float(p.pos.x) - 20, float(p.pos.y) - 20))
                  elif p.value%4 == 2:
                    screen.blit(listDrawPokemons[2], (float(p.pos.x) - 20, float(p.pos.y) - 20))
                  else:
                    screen.blit(listDrawPokemons[3], (float(p.pos.x) - 20, float(p.pos.y) - 20))

        # update screen changes
        display.update()

        # refresh rate
        clock.tick(10)

        # print("here!!!")
        # choose next edge
        try:
            game.update_game_info()
        except Exception:
            print("there is no pokemons now")

        # try:
        game.update_dest_value_per_second()
        # game.update_dest_for_agents_by_tsp_test()
        # game.update_dest_value_per_second()
        # except Exception:
        #     # game.update_dest_for_agents()

    except ConnectionResetError:
        print("Game over")


# game over:
