import unittest
from koala_formatter.formatters.graph_objects.graph_object_base import GraphObjectBase
from koala_formatter.exceptions.exceptions import InvalidGraphObject
from tests.koala_formatter.graph_objects.test_utils import NODE_INVALID, REQUIRED_FIELDS


class TestGraphObjectBase(unittest.TestCase):

    def test__validate_required_object_fields(self):
        with self.assertRaises(InvalidGraphObject):
            GraphObjectBase(obj=NODE_INVALID, required_fields=REQUIRED_FIELDS)
