NODE_VALID = {"field1": "test_value1",
              "field2": "test_value2"}

EXPECTED_NODE_AS_JSON = {"id": "test_value1.test_value2",
                         "label": "test_type",
                         "properties": {"field1": "test_value1",
                                        "field2": "test_value2",
                                        "host": "host",
                                        "type": "test_type"}}
EDGE = {"in": "in_node",
        "out": "out_node",
        "label": "memberOf"}

REQUIRED_EDGE_FIELDS = ["in", "out", "label"]

NODE_INVALID = {"field1": "test_value1"}

NODE_TYPE = "test_type"

REQUIRED_FIELDS = ("field1", "field2")

HOST_NAME = "host"


def node_id_creator():
    return lambda node: f"{node['field1']}.{node['field2']}"
