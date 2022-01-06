# EX4-OOP
python implementation for Directed Weighted Graphs and Algorithms

![image](https://user-images.githubusercontent.com/79406881/147505114-0ff881c2-fccb-45fc-9cb5-acd41036d855.png)


Graphs and graphs-algorithms explanations:

### Class Edge : This class represents the edges between two nodes , source and destinations in the graph.

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


### Class GraphToDisplay: holds an array of nods and of edges , this class is helping us to save and load to json because any json file holds edges and nodes, this class also help us to represent a node to a json file as we want , therefore holds also a class of NodeToDisplay.

### Class PriorityQueue: a class that is implementing a priorityQueue which has the functions isEmpty, insert, size, delete. this priorityqueue is giving priority to the node with the minimum weight.To read more about the functions above https://docs.oracle.com/javase/7/docs/api/java/util/PriorityQueue.html

### Class PlottingRes: this class is plotting and compering our reasults by using matplotlib library between java and paython.

## GUI explanations:

After loading the graph there is a screen that we created by using pygame.

In this screen we have several options that we created in the bar , by using buttons.

<img width="140" alt="image" src="https://user-images.githubusercontent.com/79164312/147508868-dc25ce8f-e148-433a-8037-94018bef01a2.png">

Center – by pressing the center button the center will be painted with a green circle.

<img width="644" alt="image" src="https://user-images.githubusercontent.com/79164312/147508937-dc2e9d69-7038-42cb-925f-a7b24a757e22.png">

Tsp = by pressing the tsp button  a second screen will be open and you will be requested to insert the node list, after that it will draw the rout on the graph.

<img width="320" alt="image" src="https://user-images.githubusercontent.com/79164312/147509005-7f90a285-4ebb-4f94-b35c-e6df5ad10602.png">

Shortest - by pressing the shortest button  a second screen will be open and you will be requested to insert the two nodes,fter that it will draw the rout on the graph.

<img width="251" alt="image" src="https://user-images.githubusercontent.com/79164312/147509066-88570125-37b4-41d2-bb5b-3e05b3dc6e9c.png">

### We did it by building 2 classes:

graph_gui – this is the class which is showing the screen , normalizing the graph and drawing the graph and the buttons and the lines.

gui input – this class is showing the input screen which by using him we are getting the nodes to use the tsp or the shortest path algorithems.

<img width="478" alt="image" src="https://user-images.githubusercontent.com/79164312/147509354-5771ed2d-c046-49e8-ba84-ebab22b3e29a.png">

NOTE : we also added a function that while searching the shortest path between the nodes(while running shortest path algorithm or tsp) we drawing the path and showing the weight of the edge. This is happening also when we are adding an edge. We also showing the node while adding it and the center while searching it.
