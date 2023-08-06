from collections.abc import Callable
from koala_formatter.formatters import utils
from koala_formatter.formatters.formatter_base import FormatterBase


class KafkaFormatter(FormatterBase):

    def __init__(self, db_url: str = None):
        super().__init__()
        self._host = utils.get_host(db_url)

    def __enter__(self):
        return self

    @property
    def collection_node_type(self):
        return "kafka_topic"

    @property
    def required_collection_node_fields(self):
        return ("topic_name",)

    @property
    def resource_node_type(self):
        return "kafka_topic_field"

    @property
    def required_resource_node_fields(self):
        return "topic_name", "field_name"

    @property
    def collection_id_creator(self) -> Callable:
        return lambda topic_map: f"{topic_map['topic_name']}"

    @property
    def resource_id_creator(self) -> Callable:
        return lambda topic_field_map: f"{topic_field_map['topic_name']}.{topic_field_map['field_name']}"

    @property
    def origin_host(self):
        return self._host
