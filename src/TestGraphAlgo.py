from unittest import TestCase
from GraphAlgo import *


class TestGraphAlgo(TestCase):
    def setUp(self) -> None:
        g = GraphAlgo()
        g.load_from_json(r"..\data\A1.json")
        self.gAlgo = g

    def test_is_connected(self):
        self.assertEqual(self.gAlgo.isConnected(), True)

    def test_nodes_edges_to_display(self):
        gDisplay = self.gAlgo.nodesEdgesToDisplay(self.gAlgo.graph)
        ans = gDisplay.Edges[0].weight
        self.assertEqual(ans, 1.3118716362419698)
        ans = gDisplay.Nodes[0].pos
        self.assertEqual(ans, "35.19589389346247,32.10152879327731,0.0")

    def test_shortest_path(self):
        ans = self.gAlgo.shortest_path(3, 11)
        sum = 10.158987256710258
        self.assertEqual(ans[0], sum)

    def test_tsp(self):
        ans = self.gAlgo.TSP([7, 5, 3, 12])
        self.assertEqual(ans[1], 12.98663305159289)

    def test_center_point(self):
        ans = self.gAlgo.centerPoint()
        self.assertEqual(ans[0], 8)
        self.assertEqual(ans[1], 9.925289024973141)
