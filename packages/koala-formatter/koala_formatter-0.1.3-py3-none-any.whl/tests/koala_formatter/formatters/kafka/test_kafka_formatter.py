import unittest

from koala_formatter.formatters.kafka.kafka_formatter import KafkaFormatter
from tests.koala_formatter.formatters.kafka.test_utils.properties import EXPECTED_COLLECTION_NODE_TYPE, \
    EXPECTED_RESOURCE_NODE_TYPE, EXPECTED_REQUIRED_COLLECTION_NODE_FIELDS, EXPECTED_REQUIRED_RESOURCE_NODE_FIELDS
from tests.koala_formatter.formatters.kafka.test_utils.nodes import COLLECTION_NODES, RESOURCE_NODES,\
    EXPECTED_COLLECTION_ID, EXPECTED_RESOURCE_ID


class TestKafkaFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = KafkaFormatter()

    def test_collection_node_type(self):
        collection_type = self.formatter.collection_node_type
        self.assertEqual(EXPECTED_COLLECTION_NODE_TYPE, collection_type)

    def test_resource_node_type(self):
        resource_type = self.formatter.resource_node_type
        self.assertEqual(EXPECTED_RESOURCE_NODE_TYPE, resource_type)

    def test_required_collection_node_fields(self):
        required_collection_fields = self.formatter.required_collection_node_fields
        self.assertEqual(EXPECTED_REQUIRED_COLLECTION_NODE_FIELDS, required_collection_fields)

    def test_required_resource_node_fields(self):
        required_resource_fields = self.formatter.required_resource_node_fields
        self.assertEqual(EXPECTED_REQUIRED_RESOURCE_NODE_FIELDS, required_resource_fields)

    def test_collection_id_creator(self):
        collection_id = self.formatter.collection_id_creator(COLLECTION_NODES)
        self.assertEqual(EXPECTED_COLLECTION_ID, collection_id)

    def test_resource_id_creator(self):
        resource_id = self.formatter.resource_id_creator(RESOURCE_NODES)
        self.assertEqual(EXPECTED_RESOURCE_ID, resource_id)
