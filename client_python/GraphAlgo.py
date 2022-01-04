import sys
from typing import List
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from client_python.GraphInterface import GraphInterface
from Node import Node
from PriorityQueue import PriorityQueue
import json
import random
from Edge import Edge


# from GraphToDisplay import NodeToDisplay
# from GraphToDisplay import GraphToDisplay

# from graph_gui import *
# from src.graph_gui import Gui


def checkIfAllBlack(graph) -> bool:
    for checkColorNode in graph.Nodes.values():
        if checkColorNode.tag != DiGraph.BLACK:
            return False
    return True


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=None):
        self.graph = graph

    # get - THERE IS NO NEED
    # set - THERE IS NO NEED
    # is connected ?
    # BFS ? - DID IT
    # dijkstra did it
    # get path after dijkstra did it
    #

    def BFS(self, g: DiGraph, node) -> None:
        WHITE = 0
        GREY = 1
        BLACK = 2
        g.Nodes.get(node).tag = GREY
        queue = [node]
        while queue:
            id = queue.pop()
            for dest, w in g.all_out_edges_of_node(id).items():
                if g.Nodes.get(dest).tag == WHITE:
                    nextId = dest
                    g.Nodes.get(nextId).tag = GREY
                    queue.append(nextId)
            g.Nodes.get(id).tag = BLACK

    def isConnected(self) -> bool:
        self.graph.colorWhite()  ## make the func
        if self.graph.v_size() < 2:
            return True
        key = list(self.graph.Nodes.keys())[0]
        self.BFS(self.graph, key)
        if not checkIfAllBlack(self.graph):
            return False
        tGraph = self.graph.transpose()
        tGraph.colorWhite()
        self.BFS(tGraph, key)
        if not checkIfAllBlack(tGraph):
            return False
        return True

    def load_from_json(self, json_string: str) -> bool:
        try:
            dGraph = DiGraph()
            json_dict = json.loads(json_string)
            for n in json_dict['Nodes']:
                if "pos" in n:
                    loc = n["pos"].split(',')
                    dGraph.add_node(node_id=n["id"], pos=(float(loc[0]), float(loc[1]), float(loc[2])))
                else:
                    dGraph.add_node(node_id=n["id"])

            for e in json_dict["Edges"]:
                dGraph.add_edge(id1=e['src'], id2=e['dest'], weight=e['w'])

            self.__init__(dGraph)
            return True
        except:
            return False

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "w") as f:
                gDisplay = self.nodesEdgesToDisplay(self.graph)
                json.dump(gDisplay, fp=f, indent=2, default=lambda o: o.__dict__)
            return True
        except:
            return False

    # def nodesEdgesToDisplay(self, graph):
    #     gDisplay = GraphToDisplay()
    #     for node in graph.Nodes.values():
    #         posAsString = str(node.pos.x) + "," + str(node.pos.y) + "," + "{:.1f}".format(node.pos.z)
    #         newNode = NodeToDisplay(posAsString, node.id)
    #         gDisplay.Nodes.append(newNode)
    #     for e in graph.Edges.values():
    #         gDisplay.Edges.append(e)
    #     return gDisplay

    def shortest_path(self, id1: int, id2: int) -> (
            float, list):  ## check if first src and second dest (not nesscerry connected)
        pointers = self.dijkstra(id1)
        path = self.getPath(pointers, id1, id2)
        if path is None:
            return float("inf"), []
        pathInt = self.nodesListToIntLis(path)
        return self.graph.Nodes.get(id2).weight, pathInt

    def getPath(self, pointers, src, dst) -> List:
        try:
            path = []
            prev = dst
            while prev != src:
                if prev == -1 or prev is None:
                    return None
                path.insert(0, self.graph.Nodes.get(prev))
                prev = pointers.get(prev)
            path.insert(0, self.graph.Nodes.get(src))
            return path
        except:
            return None

    # def plot_graph(self) -> None:
    #     Gui(self)

    def dijkstra(self, src):  ## check if weight is positive
        pqueue = PriorityQueue()
        prevPointer = {}  ## key = id node, val= point to(node)
        for node in self.graph.Nodes.values():
            if node.id == src:
                node.weight = 0
                prevPointer[node.id] = None
            else:
                node.weight = sys.maxsize
                prevPointer[node.id] = -1
            pqueue.insert(node)
        while not pqueue.isEmpty():
            currNode = pqueue.delete()
            for (nodeNeighbourID, weight) in self.graph.all_out_edges_of_node(currNode.id).items():
                # nodeNeighbourID = self.graph.Nodes.get(edge.dest)
                newWeight = currNode.weight + weight
                if newWeight < self.graph.Nodes.get(nodeNeighbourID).weight:
                    self.graph.Nodes.get(nodeNeighbourID).weight = newWeight
                    prevPointer[nodeNeighbourID] = currNode.id
        return prevPointer

    def get_graph(self) -> GraphInterface:
        return self.graph
        """
        :return: the directed graph on which the algorithm works on.
        """

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        try:
            flag = True
            for i in range(len(node_lst)):
                try:
                    tmp = list(self.graph.Nodes.keys())[i]
                except:
                    flag = False
                    break
            if not flag:
                print("There is no such key! try again")
                return None
            totalDist = 0
            ansNodes = []  ## nodes
            tGraph = self.graph.transpose()
            original = self
            transpose = GraphAlgo(tGraph)
            ansNodes.append(self.graph.Nodes.get(node_lst[0]))  ## The node
            del node_lst[0]
            while len(node_lst) > 0:
                dij_original_pointers = original.dijkstra(ansNodes[-1].id)
                dij_transpose_pointers = transpose.dijkstra(ansNodes[0].id)
                endMinWeight = sys.maxsize
                endMinWeightKey = -1
                for nodeKey in node_lst:
                    currNode = self.graph.Nodes.get(nodeKey)
                    if currNode.weight < endMinWeight:
                        endMinWeight = currNode.weight
                        endMinWeightKey = currNode.id

                startMinWeight = sys.maxsize
                startMinWeightKeyNode = -1
                for nodeKey in node_lst:
                    currNode = transpose.graph.Nodes.get(nodeKey)
                    if currNode.weight < startMinWeight:
                        startMinWeight = currNode.weight
                        startMinWeightKeyNode = currNode.id

                if endMinWeight < startMinWeight:
                    tmpList = self.getPath(dij_original_pointers, ansNodes[-1].id, endMinWeightKey)
                    del tmpList[0]
                    for node in tmpList:
                        ansNodes.append(node)
                        # totalDist += ansNodes[-2].weight - ansNodes[-1].weight
                        totalDist += self.graph.Edges[str(ansNodes[-2].id) + "," + str(ansNodes[-1].id)].weight
                        # totalDist += ansNodes[-1].weight - ansNodes[-2].weight
                    node_lst.remove(endMinWeightKey)
                else:
                    tmpList = transpose.getPath(dij_transpose_pointers, ansNodes[0].id, startMinWeightKeyNode)
                    del tmpList[0]
                    for i in range(len(tmpList)):
                        ansNodes.insert(0, original.graph.Nodes.get(tmpList[i].id))
                        totalDist += self.graph.Edges[str(ansNodes[0].id) + "," + str(ansNodes[1].id)].weight
                        # totalDist += ansNodes[0].weight - ansNodes[1].weight
                        # totalDist += ansNodes[1].weight - ansNodes[0].weight
                    node_lst.remove(startMinWeightKeyNode)
                for nodeId in node_lst:
                    for node in ansNodes:
                        if node.id == nodeId:
                            node_lst.remove(nodeId)
            ans = self.nodesListToIntLis(ansNodes)
            return ans, totalDist
        except:
            return None

    def nodesListToIntLis(self, nodeList) -> List:
        listAns = []
        for node in nodeList:
            listAns.append(node.id)
        return listAns

        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float):  ## why if not connected we canot find center

        if not self.isConnected():
            return None, float("inf")
        minMaxNode = None
        bestMinMax = sys.maxsize  ## maxNum
        for node in self.graph.Nodes.values():
            self.dijkstra(node.id)
            tmpMaxDist = -sys.maxsize - 1
            for checkNode in self.graph.Nodes.values():
                if checkNode.weight > tmpMaxDist:
                    tmpMaxDist = checkNode.weight
            if tmpMaxDist < bestMinMax:
                bestMinMax = tmpMaxDist
                minMaxNode = node
        return minMaxNode.id, bestMinMax

        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """


if __name__ == '__main__':
    # pqueue = PriorityQueue()
    # node1 = Node(5, None, 5, {}, {}, 1)
    # node2 = Node(3, None, 7, {}, {}, 1)
    # node3 = Node(1, None, 1, {}, {}, 1)
    # node4 = Node(6, None, 2, {}, {}, 1)
    # node5 = Node(34, None, 12, {}, {}, 1)
    # pqueue.insert(node5)
    # pqueue.insert(node3)
    # pqueue.insert(node1)
    # pqueue.insert(node2)
    # pqueue.insert(node4)
    # while not pqueue.isEmpty():
    #     print(pqueue.delete().weight)
    # g = DiGraph()
    # edgesOut = {}
    # for src in range(10):
    #     for dst in range(src):
    #         if src !=dst:
    #             stringName = str(src)+','+str(dst)
    #             x = random.uniform(0,10)
    #             e = Edge(src, x, dst)
    #             g.Edges[stringName]=e
    #
    #
    # for i in range(10):
    #     x , y = random.uniform(0,100) , random.uniform(0,100)
    #     g.Nodes[i] = Node(i,(x,y,0))

    gAlgo = GraphAlgo()
    g = gAlgo.load_from_json(r"..\data\T0.json")
    # gAlgo = GraphAlgo(g)
    # gAlgo.save_to_json(r"..\data\test.json")
    gAlgo.plot_graph()
