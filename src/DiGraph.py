from GraphInterface import GraphInterface
from src.Edge import Edge
from src.Node import Node
from src.Location import Location


class DiGraph(GraphInterface):
    WHITE = 0
    GREY = 1
    BLACK = 2

    def __init__(self):
        self.Nodes = {}  # key = id, value = node
        self.Edges = {}  # key = "src,dest" , value = edge
        self.mc = 0

    # ge set methods

    def v_size(self) -> int:
        return len(self.Nodes)

    def e_size(self) -> int:
        return len(self.Edges)

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        self.Nodes.get(id1).add_edge_out(id2, weight)
        self.Nodes.get(id2).add_edge_in(id1, weight)
        e = Edge(src=id1, dest=id2, w=weight)
        e_name = str(id1) + ',' + str(id2)
        self.Edges[e_name] = e
        self.mc+=1

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if pos is None:
            loc = Location()
        else:
            loc = Location(pos[0], pos[1], pos[2])
        n = Node(_id=node_id, pos=loc)
        self.Nodes[node_id] = n
        self.mc += 1

    def add_exist_node(self, node: Node):
        self.Nodes[node.id] = node
        self.mc += 1

    def remove_node(self, node_id: int) -> bool:
        is_removed = self.Nodes.pop(node_id)
        if is_removed is None:
            print("there is no such key!")
            return False
        else:
            for key in list(self.Edges.keys()):
                src = key.split(',')[0]
                dest = key.split(',')[1]
                if src == str(node_id):
                    self.remove_edge(int(src), int(dest))
                    self.Nodes.get(int(dest)).remove_edge_in(int(src))
                elif dest == str(node_id):
                    self.remove_edge(int(src), int(dest))
                    self.Nodes.get(int(src)).remove_edge_out(int(dest))
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        name = str(node_id1) + ',' + str(node_id2)
        is_removed = self.Edges.pop(name)
        if is_removed is None:
            return False
        else:
            self.mc += 1
            return True

    """return a dictionary of all the nodes in the Graph, each node is represented using a pair
             (node_id, node_data)
            """

    def get_all_v(self) -> dict:
        data_dict = {}
        for key, value in self.Nodes.items():
            data_dict[key] = str(value)
        return data_dict

    """return a dictionary of all the nodes connected to (into) node_id ,
            each node is represented using a pair (other_node_id, weight)
             """
    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.Nodes.get(id1).edges_in

    """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
            (other_node_id, weight)
            """

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.Nodes.get(id1).edges_out

    # copy
    # color white
    def colorWhite(self):
        for node in self.Nodes.values():
            node.tag = 0  # WHITE

# transpose
    def transpose(self):
        T_graph = DiGraph()
        for node in self.Nodes.values():
            T_graph.add_node(node_id=node.id, pos=(node.pos.x, node.pos.y, node.pos.z))

        for edge in self.Edges.values():
            T_graph.add_edge(id1=edge.dest, id2=edge.src, weight=edge.weight)

        return T_graph

    def __str__(self):
        s = "Graph: |V|=" + str(self.v_size()) + ", |E|=" + str(self.e_size())
        return s
