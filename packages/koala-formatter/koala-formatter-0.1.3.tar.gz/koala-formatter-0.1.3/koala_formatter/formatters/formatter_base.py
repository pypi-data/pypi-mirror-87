import sys
import logging
from abc import ABC, abstractmethod
from collections.abc import MutableSequence, Sequence
from koala_formatter.formatters.graph_objects.graph_edge import GraphEdge
from koala_formatter.formatters.graph_objects.graph_node import GraphNode


class FormatterBase(ABC):
    """ Base class for formatting data resource collections with associated resources and creating the
        corresponding graph nodes and edges

        Examples:
            - Database tables (collections), table columns (resources)
            - Kafka topics (collections), topic fields (resources)
    """

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))

    def __enter__(self):
        return self

    @property
    @abstractmethod
    def collection_node_type(self):
        return NotImplementedError()

    @property
    @abstractmethod
    def required_collection_node_fields(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def resource_node_type(self):
        return NotImplementedError()

    @property
    @abstractmethod
    def required_resource_node_fields(self):
        raise NotImplementedError()

    @property
    def required_edge_fields(self):
        return 'inV', 'outV', 'label'

    @property
    @abstractmethod
    def collection_id_creator(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def resource_id_creator(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def origin_host(self):
        raise NotImplementedError()

    def create_nodes(self, collections, resources) -> Sequence:
        collection_nodes, resource_nodes = self._create_nodes(collections, resources)
        edges = self._create_edges(resources)
        return collection_nodes, resource_nodes, edges

    def _create_nodes(self, collections, resources) -> Sequence:
        collection_nodes = self._create_collection_nodes(collections)
        resource_nodes = self._create_resource_nodes(resources)
        return collection_nodes, resource_nodes

    def _create_collection_nodes(self, collections) -> MutableSequence:
        return [GraphNode(collection,
                          self.collection_node_type,
                          self.required_collection_node_fields,
                          self.collection_id_creator,
                          self.origin_host).as_json() for collection in collections]

    def _create_resource_nodes(self, resources) -> MutableSequence:
        return [GraphNode(resource,
                          self.resource_node_type,
                          self.required_resource_node_fields,
                          self.resource_id_creator,
                          self.origin_host).as_json() for resource in resources]

    def _create_edges(self, resources):
        edges = []
        for resource in resources:
            edges += self._create_resource_edges(resource)
        return edges

    def _create_resource_edges(self, resource) -> Sequence:
        return [
            GraphEdge(edge={
                "inV": self.collection_id_creator(resource),
                "outV": self.resource_id_creator(resource),
                "label": "memberOf"
            }, required_fields=self.required_edge_fields).as_json(),

            GraphEdge(edge={
                "inV": self.resource_id_creator(resource),
                "outV": self.collection_id_creator(resource),
                "label": "hasMember"
            }, required_fields=self.required_edge_fields).as_json()
        ]

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
