import unittest

from koala_formatter.formatters.db.tableau_formatter import TableauFormatter
from tests.koala_formatter.formatters.db.test_utils.properties import TABLEAU_EXPECTED_COLLECTION_NODE_TYPE, \
    TABLEAU_EXPECTED_RESOURCE_NODE_TYPE, TABLEAU_EXPECTED_REQUIRED_COLLECTION_NODE_FIELD, \
    TABLEAU_EXPECTED_REQUIRED_RESOURCE_NODE_FIELD
from tests.koala_formatter.formatters.db.test_utils.nodes import TABLEAU_COLLECTIONS, TABLEAU_RESOURCES


class TestTableauFormatter(unittest.TestCase):

    def setUp(self):
        self.formatter = TableauFormatter()

    def test_collection_node_type(self):
        collection_node_type = self.formatter.collection_node_type
        self.assertEqual(TABLEAU_EXPECTED_COLLECTION_NODE_TYPE, collection_node_type)

    def test_resource_node_type(self):
        resource_node_type = self.formatter.resource_node_type
        self.assertEqual(TABLEAU_EXPECTED_RESOURCE_NODE_TYPE, resource_node_type)

    def test_required_collection_node_fields(self):
        collection_required_node_fields = self.formatter.required_collection_node_fields
        self.assertEqual(TABLEAU_EXPECTED_REQUIRED_COLLECTION_NODE_FIELD, collection_required_node_fields)

    def test_required_resource_node_fields(self):
        resource_required_node_fields = self.formatter.required_resource_node_fields
        self.assertEqual(TABLEAU_EXPECTED_REQUIRED_RESOURCE_NODE_FIELD, resource_required_node_fields)

    def test_collection_id_creator(self):
        collection = TABLEAU_COLLECTIONS[0]
        collection_id = self.formatter.collection_id_creator(collection)
        expected_collection_id = f"Tableau.{collection['project_name']}.{collection['workbook_name']}".upper()
        self.assertEqual(expected_collection_id, collection_id)

    def test_resource_id_creator(self):
        resource = TABLEAU_RESOURCES[0]
        resource_id = self.formatter.resource_id_creator(resource)
        expected_resource_id = f"Tableau.{resource['project_name']}.{resource['workbook_name']}." \
                               f"{resource['view_name']}".upper()

        self.assertEqual(expected_resource_id, resource_id)
