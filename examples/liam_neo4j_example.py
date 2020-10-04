import pdb
from py2neo import Graph
from py2neo.matching import *

"""
docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --env='NEO4JLABS_PLUGINS=["apoc", "n10s"]' --env=NEO4J_AUTH=none neo4j:latest
"""

# g = Graph("bolt://localhost:7687", user="neo4j", password="neo")
g = Graph("bolt://localhost:7687")
try:
    g.run('CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE')
except Exception:
    print("Unique Constrain on r:Resource already exists")

print("Clean up graph...")
g.run('MATCH (n) DETACH DELETE n')

print("Graph config drop...")
g.run('call n10s.graphconfig.drop')


print("Graph init...")
g.run("call n10s.graphconfig.init({handleVocabUris: 'IGNORE'})")
graph_config = g.run('call n10s.graphconfig.show()').data()
handleRDFTypes = [c for c in graph_config if c.get('param') == 'handleRDFTypes']
print(graph_config)


# load_brick_1_1_ontology = 'CALL n10s.onto.import.fetch("https://brickschema.org/schema/1.1/Brick.ttl", "Turtle");'
# load_ontology_results = g.run(load_brick_1_1_ontology).data()
pdb.set_trace()

input_turtle = 'https://raw.githubusercontent.com/iamliamc/Brick/personal-experiments/examples/custom_brick_v11_sample_graph.ttl'
print(f"Importing {input_turtle}")
# This works... 
import_custom_example = f'CALL n10s.rdf.import.fetch("{input_turtle}", "Turtle");'
results = g.run(import_custom_example).data()

building = g.nodes.match('Building', BuildingUUID="0cdd624f-6a95-4c7e-b289-348621d39020").first()
buildings_relationships = list(g.relationships.match((building, None), 'hasPart').limit(3))
one_relation = buildings_relationships[0]

"""
    MATCH (n)-[:hasPart]->(part) RETURN n, part
"""
# Is equivalent to: 
res = list(g.relationships.match((None, None), 'hasPart'))
ahu = g.nodes.match('Air_Handler_Unit').first()
ahu_has_points = g.relationships.match((ahu, None), 'hasPoint').first()

all_ahu_relations_and_related_nodes = g.run("MATCH (n:Air_Handler_Unit)-[z]->(o) return n, z, o").data()

pdb.set_trace()

if False:
    g.delete_all()