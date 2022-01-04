import json
from client_python.Location import Location


def get_agents_objects(json_string):
    agents_list = []
    print(json_string)
    json_dict = json.loads(json_string)

    for agent_dict in json_dict['Agents']:
        agents_list.append(Agent(agent_dict))

    return agents_list


class Agent:

    def __init__(self, agent_dict):
        self.id = agent_dict['Agent']['id']
        self.value = agent_dict['Agent']['value']
        self.src = agent_dict['Agent']['src']
        self.dest = agent_dict['Agent']['dest']
        self.speed = agent_dict['Agent']['speed']
        loc = agent_dict['Agent']["pos"].split(',')
        self.pos = Location(float(loc[0]), float(loc[1]), float(loc[2]))
