import unittest

from koala_formatter.formatters.db.postgres_formatter import PostgresFormatter
from tests.koala_formatter.formatters.db.test_utils.properties import \
    POSTGRES_EXPECTED_COLLECTION_NODE_TYPE, POSTGRES_EXPECTED_RESOURCE_NODE_TYPE, \
    ORACLE_POSTGRES_EXPECTED_REQUIRED_RESOURCE_NODE_FIELDS, ORACLE_POSTGRES_EXPECTED_REQUIRED_COLLECTION_NODE_FIELDS
from tests.koala_formatter.formatters.db.test_utils.nodes import ORACLE_POSTGRES_COLLECTIONS, ORACLE_POSTGRES_RESOURCES


class TestPostgresFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = PostgresFormatter()

    def test_collection_node_type(self):
        collection_node_type = self.formatter.collection_node_type
        self.assertEqual(POSTGRES_EXPECTED_COLLECTION_NODE_TYPE, collection_node_type)

    def test_resource_node_type(self):
        resource_node_type = self.formatter.resource_node_type
        self.assertEqual(POSTGRES_EXPECTED_RESOURCE_NODE_TYPE, resource_node_type)

    def test_required_resource_node_fields(self):
        required_resource_node_fields = self.formatter.required_resource_node_fields
        self.assertEqual(ORACLE_POSTGRES_EXPECTED_REQUIRED_RESOURCE_NODE_FIELDS, required_resource_node_fields)

    def test_required_collection_node_fields(self):
        required_collection_node_fields = self.formatter.required_collection_node_fields
        self.assertEqual(ORACLE_POSTGRES_EXPECTED_REQUIRED_COLLECTION_NODE_FIELDS, required_collection_node_fields)

    def test_collection_id_creator(self):
        collection = ORACLE_POSTGRES_COLLECTIONS[0]
        collection_id = self.formatter.collection_id_creator(collection)
        expected_collection_id = f"{collection['db_name']}.{collection['schema_name']}.{collection['table_name']}"
        self.assertEqual(expected_collection_id, collection_id)

    def test_resource_id_creator(self):
        resource = ORACLE_POSTGRES_RESOURCES[0]
        resource_id = self.formatter.resource_id_creator(resource)
        expected_resource_id = f"{resource['db_name']}.{resource['schema_name']}.{resource['table_name']}." \
                               f"{resource['column_name']}"

        self.assertEqual(expected_resource_id, resource_id)
