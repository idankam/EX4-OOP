class Node:
    def __init__(self, _id, pos):
        self.id = _id
        self.edges_in = {}
        self.edges_out = {}
        self.pos = pos
        self.tag = -1
        self.weight = -1

    def add_edge_out(self, dest, weight):
        self.edges_out[dest] = weight

    def add_edge_in(self, src, weight):
        self.edges_in[src] = weight

    # remove edge_out
    def remove_edge_out(self, dest):
        self.edges_out.pop(dest)

    # remove edge_in
    def remove_edge_in(self, src):
        self.edges_in.pop(src)

    # remove all edges_out
    def remove_all_edges_out(self):
        self.edges_out.clear()

    def remove_all_edges_in(self):
        self.edges_in.clear()

    # copy
    def copy(self):
        new_node = Node(self.id, self.pos)
        new_node.weight = self.weight
        new_node.edges_in = self.edges_in.copy()
        new_node.edges_out = self.edges_out.copy()
        new_node.tag = self.tag
        return new_node

    def __str__(self):
        s = "id: " + str(self.id) + ", position: " + str(self.pos)
        return s
