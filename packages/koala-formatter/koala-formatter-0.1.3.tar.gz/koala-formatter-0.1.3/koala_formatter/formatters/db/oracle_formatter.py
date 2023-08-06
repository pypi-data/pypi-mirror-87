from collections.abc import Callable
from koala_formatter.formatters import utils
from koala_formatter.formatters.formatter_base import FormatterBase


class OracleFormatter(FormatterBase):

    def __init__(self, db_url: str = None):
        super().__init__()
        self._host = utils.get_host(db_url)

    def __enter__(self):
        return self

    @property
    def collection_node_type(self):
        return "oracle_table"

    @property
    def required_collection_node_fields(self):
        return 'db_name', 'schema_name', 'table_name', 'table_description', 'team_name'

    @property
    def resource_node_type(self):
        return "oracle_column"

    @property
    def required_resource_node_fields(self):
        return 'db_name', 'schema_name', 'table_name', 'column_name', 'column_description', 'data_type'

    @property
    def collection_id_creator(self) -> Callable:
        return lambda column_map: f"{column_map['db_name']}.{column_map['schema_name']}.{column_map['table_name']}"

    @property
    def resource_id_creator(self) -> Callable:
        return lambda column_map: f"{column_map['db_name']}.{column_map['schema_name']}.{column_map['table_name']}.{column_map['column_name']}"

    @property
    def origin_host(self):
        return self._host
