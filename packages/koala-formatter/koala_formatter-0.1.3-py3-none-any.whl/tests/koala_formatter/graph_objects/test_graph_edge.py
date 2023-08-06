import unittest
from koala_formatter.formatters.graph_objects.graph_edge import GraphEdge
from tests.koala_formatter.graph_objects.test_utils import EDGE, REQUIRED_EDGE_FIELDS


class TestGraphEdge(unittest.TestCase):
    def test_as_json(self):
        edge = GraphEdge(edge=EDGE, required_fields=REQUIRED_EDGE_FIELDS)
        edge_as_json = edge.as_json()
        self.assertEqual(EDGE, edge_as_json)
