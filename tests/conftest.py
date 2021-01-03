import pytest
from sdk.graph_connection import TopologyGraphDriver
from types import SimpleNamespace


@pytest.fixture(scope="function")
def sdk_graph_connection():
    return TopologyGraphDriver("neo4j://localhost:7687", "", "")


@pytest.fixture(scope="function")
def load_test_data(sdk_graph_connection):
    sdk_graph_connection.initalize_neo4j_configuration()
    if not sdk_graph_connection.is_brick_ontology_loaded():
        sdk_graph_connection.load_brick_ontology()

