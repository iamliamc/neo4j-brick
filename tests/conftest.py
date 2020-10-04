import pytest
from py2neo import Graph
from py2neo.matching import *
from sdk.graph_connection import TopologyGraphDriver
from types import SimpleNamespace


@pytest.fixture(scope="function")
def py2neo_graph_connection():
    return Graph("bolt://localhost:7687")

@pytest.fixture(scope="function")
def sdk_graph_connection():
    return TopologyGraphDriver("neo4j://localhost:7687", "", "")

@pytest.fixture(scope="function")
def load_test_data(sdk_graph_connection):
    sdk_graph_connection.initalize_neo4j_configuration()
    if not sdk_graph_connection.is_brick_ontology_loaded():
        sdk_graph_connection.load_brick_ontology()
    # # g = Graph("bolt://localhost:7687", user="neo4j", password="neo")
    # g = Graph("bolt://localhost:7687")
    # try:
    #     g.run('CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE')
    # except Exception:
    #     print("Unique Constrain on r:Resource already exists")

    # print("Clean up graph...")
    # g.run('MATCH (n) DETACH DELETE n')

    # print("Graph config drop...")
    # g.run('call n10s.graphconfig.drop')


    # print("Graph init...")
    # g.run("call n10s.graphconfig.init({handleVocabUris: 'IGNORE'})")
    # graph_config = g.run('call n10s.graphconfig.show()').data()
    # handleRDFTypes = [c for c in graph_config if c.get('param') == 'handleRDFTypes']
    # print(graph_config)


    # load_brick_1_1_ontology = 'CALL n10s.onto.import.fetch("https://brickschema.org/schema/1.1/Brick.ttl", "Turtle");'
    # load_ontology_results = g.run(load_brick_1_1_ontology).data()
    # results = sdk_graph_connection.is_brick_ontology_loaded()
    # py2neo_results = g.run('MATCH(n:Resource) where n.uri CONTAINS "https://brickschema.org/schema/1.1/Brick#" RETURN n LIMIT 10').data()
    # import pdb; pdb.set_trace()

