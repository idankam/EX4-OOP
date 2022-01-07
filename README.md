# EX4-OOP




https://user-images.githubusercontent.com/79164312/148529720-51ede0c4-4330-4beb-b369-e0f6c4e743c4.mp4



python implementation for Directed Weighted Graph Pokemon Game:

![image](https://user-images.githubusercontent.com/79164312/148466788-586c5e64-c268-4e43-84dd-87af2835a438.png)



Pkemon Game Explanetion:

### Class Edge : This class represents the edges between two nodes , source and weight in the graph.

### Class Node : This class represents a Node in the graph. The node holds an id, position, weight, the edges out (from him to another node),the edges in (from another node to him) and a tag.

#### Class Node functions:

add_edge_in – adding an edge from node to this node.

add_edge_out – adding an edge from this node to another node.

Copy – coping the object node.

remove_edge_out - removing a specific edge out of this node.

remove_edge_in - removing a specific edge in of this node.

remove_all_edges_out - removing all edges out of this node.

remove_all_edges_in - removing all edges in of this node.

__str__ – representig the node as a string.

### Class Location : This class represents the locations to each node by x axis y axis and z axis.

copy - coping the same location.

distance - calculating the distance from this node to another node.

### Class DiGraph: This class represents the Directed graph the graph holds all the nodes and all the edges.

#### Class DiGraph functions:

v_size- returning number of nodes in the graph.

edgeSize – returning number of edges in the graph.

addNode – Adding a node to the graph.

add_edge – connecting two nodes with an edge (that holds weight).

removeNode – Removing a node from the graph.

removeEdge – Removing an Edge from the graph.

get_mc – returning all the changes in the graph.

get_all_v - returning a dictionary of all the nodes in the Graph, each node is represented using a pair (node_id, node_data).

all_in_edges_of_node - return a dictionary of all the nodes connected to (into) node_id each node is represented using a pair (other_node_id, weight)

all_out_edges_of_node - return a dictionary of all the nodes connected from node_id , each node is represented using a pair (other_node_id, weight)

__str__ - returning a string representing the DiGraph.

colorWhite – iterating the nodes and changing the tag to be white(the options for the tag are three colors).

transpose – creating a transpose graph by changing the directions of the edges(that will help us with algorithms in the next class).

### Class GraphAlgo: A class that holds a DiGraph(Directed weighted Graph). This class has the algorithms we can run on the graph.

#### Class GraphAlgo functions –

Init – The constructor getting a graph an returning it.

getGraph – returning the graph.

BFS – a searching algorithm that is getting the graph and a node and painting every node he get to.

Dijkstra – this is the an algorithm that we are using to get the shortest path, this algorithm is returning the shortest paths from a node to all the other nodes. For more information: (https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm).

Is connected – a function that is checking if the graph is connected by using BFS algorithm we are checking on one node and after that using the transpose dunction and checking on the transpose if there is a rout from this node in the graph and also in the transpose graph so the graph is connected.

sortestPathDist – calling the Dijkstra algorithm and by that returning the shortest path weight.

shortest_path – calling the dijekstra and returning a tuple of list of the shortest path and float of the path.

getPath – a helper function that is putting the shortest path after using the dijekstra into a list(the dijektra returning a hushMap).

centerPoint – returning the center of the graph , the point where the longest destination of the point is the shortest (using the dijekstra algorithm).

Tsp – this algorithm is finding the shortest path between a list of nodes. We are doing it by rotating the list of cities that we are getting , every rotation we are checking the closest on by using the dijekstra and by using the transpose function we are checking what will be a shorter path to add this city to the end of the rout or to the start(we are looking for the shortest path).

save_to_json – saving the graph into a json file , using a NodeToDisplay class(helper class).

load_from_json – loading from json file.

nodesEdgesToDisplay - a helper function we are using to save the nodes into a json file with.

plot_graph - the function that is calling the Gui to plot the graph.

nodesListToIntLis -  converting node list to their id wich is int.


### Class PriorityQueue: a class that is implementing a priorityQueue which has the functions isEmpty, insert, size, delete. this priorityqueue is giving priority to the node with the minimum weight.To read more about the functions above https://docs.oracle.com/javase/7/docs/api/java/util/PriorityQueue.html

### Class TestDiGraph: for Testing the Graph.

### Class TestDiGraphAlgos: for Testing the Graph Algorithems.

## The get_pokemon_objects - reading a string as json and returning a list of pokemons.

### Class Pokemon : this class represents the pokemons that are on the Graph Each Pokemon has a Value , id , pos(position) and at which adge he is located.

#### Class GraphAlgo functions –

init - a constarctor to the fields we mantioned above.

getEdge - returning the pokemon edge.

getNode - returning the pokemon node.

is_on_edge - returning a boolean value if a node is on a specific edge.

## The get_Agent_objects - reading a string as json and returning a list of pokemons.

### Class Agent - this class represents the Agents that are capturing the Pokemons every Agent has an id , value , src , dest , speed , pos(position).

### client - a class that we got for this task( that we can not change) , this class is creating connection with the server.

### Game class - this Class holds the algorithem to capture as many pokemons as we can.

## Game class functions -

update_game_info - updating the Game information.

add_agents_to_game - adding agents to the start point the agent starts from the center if there are more then one agent they are starting from a random nodes.

update_dest_value_per_second - this is our main function for the capturing the pokemons , basiclly this function is calculeting the worthes Pokemon to got to by calculating the value of the distance (using dijakstra algorithem) and the agent speed and sending the agent to fetch him.

### Ex4 - this class is the class where the Gui is located , this class is also by while loop updating the screen for the game long. more explanations and description about the GUI below.



## GUI explanations:

while starting the game you will see immediately the screen.

![image](https://user-images.githubusercontent.com/79164312/148466788-586c5e64-c268-4e43-84dd-87af2835a438.png)

The pokemons are pectures of diffarent pokemons and the back round is pokemons backround Game as you cab see below.

<img width="637" alt="Untitled" src="https://user-images.githubusercontent.com/79164312/148469507-0e4a39ed-759e-4f07-bbc4-b62f08fe53e8.png">

The Agent is a pokemon trainer Which is "throwing" the pokeball while close enagh an "catching" the pokemons , NOTE: he is catching a pokemon only while on the "rigth diraction , if he is on the opposite edge althgh he is passing the same location he will not "throw the ball". exampel on the black circles for fetching the pokemon.

<img width="637" alt="Untitled" src="https://user-images.githubusercontent.com/79164312/148470454-0de76270-97f8-417f-95f5-9183de2c9761.png">

### We did it by using our calculations for dist putting and locating the pokemons and the agents on the right placec on the graph , scalling , and calculating the wright diractions for the pokemons.
