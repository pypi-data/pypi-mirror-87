import unittest

from koala_formatter.formatters.graph_objects.graph_node import GraphNode
from koala_formatter.exceptions.exceptions import InvalidGraphObject
from tests.koala_formatter.graph_objects.test_utils import NODE_VALID, NODE_INVALID, EXPECTED_NODE_AS_JSON, NODE_TYPE, \
    REQUIRED_FIELDS, HOST_NAME, node_id_creator


class TestGraphNode(unittest.TestCase):
    def test__create_node_id(self):
        node = GraphNode(node=NODE_VALID, node_type=NODE_TYPE, required_fields=REQUIRED_FIELDS,
                         id_creator=node_id_creator(), host_name=HOST_NAME)

        node_id = node._create_node_id(node_id_creator())
        expected_node_id = 'test_value1.test_value2'
        self.assertEqual(expected_node_id, node_id)

    def test__create_node_id_invalid(self):
        with self.assertRaises(InvalidGraphObject):
            GraphNode(node=NODE_INVALID, node_type=NODE_TYPE, required_fields=REQUIRED_FIELDS,
                      id_creator=node_id_creator(), host_name=HOST_NAME)

    def test_as_json(self):
        node = GraphNode(node=NODE_VALID, node_type=NODE_TYPE, required_fields=REQUIRED_FIELDS,
                         id_creator=node_id_creator(), host_name=HOST_NAME)

        node_json = node.as_json()

        self.assertEqual(EXPECTED_NODE_AS_JSON, node_json)

