from unittest import TestCase
from GraphAlgo import *


class TestDiGraph(TestCase):

    def setUp(self):
        a = GraphAlgo()
        a.load_from_json("../data/A5.json")
        self.graph = a.get_graph()

    def test_v_size(self):
        self.assertTrue(self.graph.v_size() == 48)

    def test_e_size(self):
        print(".graph.e_size")
        print(self.graph.e_size())
        self.assertTrue(self.graph.e_size() == 166)

    def test_add_edge(self):
        before = self.graph.e_size()
        self.graph.add_edge(1, 40, 1.1)
        after = self.graph.e_size()
        self.assertTrue(before + 1 == after)

    def test_add_node(self):
        before = self.graph.v_size()
        self.graph.add_node(70)
        after = self.graph.v_size()
        self.assertTrue(before + 1 == after)

    def test_remove_node(self):
        before = self.graph.v_size()
        self.graph.remove_node(1)
        after = self.graph.v_size()
        self.assertTrue(before - 1 == after)

    def test_remove_edge(self):
        before = self.graph.e_size()
        self.graph.remove_edge(1, 2)
        after = self.graph.e_size()
        self.assertTrue(before - 1 == after)

    def test_get_all_v(self):
        nodes = self.graph.get_all_v()
        self.assertTrue(len(nodes) == self.graph.v_size())

    def test_all_in_edges_of_node(self):
        e = self.graph.all_in_edges_of_node(0)
        print(len(e))
        self.assertTrue(len(e) == 4)

    def test_all_out_edges_of_node(self):
        e = self.graph.all_out_edges_of_node(0)
        print(len(e))
        self.assertTrue(len(e) == 4)
