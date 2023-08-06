import unittest

from koala_formatter.formatters.db.oracle_formatter import OracleFormatter
from tests.koala_formatter.formatters.db.test_utils.nodes import ORACLE_POSTGRES_COLLECTIONS, ORACLE_POSTGRES_RESOURCES
from tests.koala_formatter.formatters.db.test_utils.properties import HOST_URL, ORACLE_EXPECTED_RESOURCE_NODE_TYPE,\
    ORACLE_EXPECTED_COLLECTION_NODE_TYPE, ORACLE_POSTGRES_EXPECTED_REQUIRED_COLLECTION_NODE_FIELDS, \
    ORACLE_POSTGRES_EXPECTED_REQUIRED_RESOURCE_NODE_FIELDS, EXPECTED_HOST_URL
from tests.koala_formatter.formatters.db.test_utils.expected_nodes import ORACLE_EXPECTED_COLLECTION_NODES, \
    ORACLE_EXPECTED_RESOURCE_NODES
from tests.koala_formatter.formatters.db.test_utils.expected_edges import ORACLE_POSTGRES_EXPECTED_EDGES


class TestOracleFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = OracleFormatter(HOST_URL)

    def test_resource_id_creator(self):
        resource = ORACLE_POSTGRES_RESOURCES[0]
        resource_id = self.formatter.resource_id_creator(resource)
        expected_resource_id = f"{resource['db_name']}.{resource['schema_name']}.{resource['table_name']}." \
                               f"{resource['column_name']}"

        self.assertEqual(expected_resource_id, resource_id)

    def test_collection_id_creator(self):
        collection = ORACLE_POSTGRES_COLLECTIONS[0]
        collection_id = self.formatter.collection_id_creator(collection)
        expected_collection_id = f"{collection['db_name']}.{collection['schema_name']}.{collection['table_name']}"

        self.assertEqual(expected_collection_id, collection_id)

    def test__create_resource_nodes(self):
        resource_nodes = self.formatter._create_resource_nodes(ORACLE_POSTGRES_RESOURCES)
        self.assertEqual(ORACLE_EXPECTED_RESOURCE_NODES, resource_nodes)

    def test__create_collection_nodes(self):
        collection_nodes = self.formatter._create_collection_nodes(ORACLE_POSTGRES_COLLECTIONS)
        self.assertEqual(ORACLE_EXPECTED_COLLECTION_NODES, collection_nodes)

    def test__create_resource_edges(self):
        resource = ORACLE_POSTGRES_RESOURCES[0]
        edges = self.formatter._create_resource_edges(resource)
        expected_edges = ORACLE_POSTGRES_EXPECTED_EDGES[0:2]
        self.assertEqual(expected_edges, edges)

    def test__create_edges(self):
        edges = self.formatter._create_edges(ORACLE_POSTGRES_RESOURCES)
        self.assertEqual(ORACLE_POSTGRES_EXPECTED_EDGES, edges)

    def test_collection_node_type(self):
        collection_node_type = self.formatter.collection_node_type
        self.assertEqual(ORACLE_EXPECTED_COLLECTION_NODE_TYPE, collection_node_type)

    def test_required_collection_node_fields(self):
        required_collection_node_fields = self.formatter.required_collection_node_fields
        self.assertEqual(ORACLE_POSTGRES_EXPECTED_REQUIRED_COLLECTION_NODE_FIELDS, required_collection_node_fields)

    def test_resource_node_type(self):
        resource_node_type = self.formatter.resource_node_type
        self.assertEqual(ORACLE_EXPECTED_RESOURCE_NODE_TYPE, resource_node_type)

    def test_required_resource_node_fields(self):
        required_resource_node_fields = self.formatter.required_resource_node_fields
        self.assertEqual(ORACLE_POSTGRES_EXPECTED_REQUIRED_RESOURCE_NODE_FIELDS, required_resource_node_fields)

    def test_origin_host(self):
        host = self.formatter.origin_host

        self.assertEqual(EXPECTED_HOST_URL, host)

    def test_create_nodes(self):
        collections_nodes, resources_nodes, edges = self.formatter.create_nodes(ORACLE_POSTGRES_COLLECTIONS,
                                                                                ORACLE_POSTGRES_RESOURCES)

        self.assertEqual(ORACLE_EXPECTED_RESOURCE_NODES, resources_nodes)
        self.assertEqual(ORACLE_EXPECTED_COLLECTION_NODES, collections_nodes)
        self.assertEqual(ORACLE_POSTGRES_EXPECTED_EDGES, edges)

