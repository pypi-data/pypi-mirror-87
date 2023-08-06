from typing import Callable
from koala_formatter.formatters import utils
from koala_formatter.formatters.formatter_base import FormatterBase


class TableauFormatter(FormatterBase):

    def __init__(self, host_address: str=None):
        super().__init__()
        self._host = utils.get_host(host_address)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def collection_node_type(self):
        return "tableau_workbook"

    @property
    def required_collection_node_fields(self):
        return 'project_name', 'workbook_name', 'issued', 'modified'

    @property
    def resource_node_type(self):
        return "tableau_view"

    @property
    def required_resource_node_fields(self):
        return 'project_name', 'workbook_name', 'contentUrl', "view_name", "preview"

    @property
    def collection_id_creator(self) -> Callable:
        return lambda node_map: f"Tableau.{node_map['project_name']}.{node_map['workbook_name']}".upper()

    @property
    def resource_id_creator(self) -> Callable:
        return lambda node_map: f"Tableau.{node_map['project_name']}.{node_map['workbook_name']}.{node_map['view_name']}".upper()

    @property
    def origin_host(self):
        return self._host
