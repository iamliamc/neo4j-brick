import rdf2g
import rdflib
import pathlib
import pdb
from pprint import pprint

"""docker run --name janusgraph-default -p 8182:8182 janusgraph/janusgraph:latest"""
"""docker run --name gremlin-server -p 5566:8182 tinkerpop/gremlin-server"""

DEFAULT_LOCAL_CONNECTION_STRING = "ws://localhost:8182/gremlin"
g = rdf2g.setup_graph(DEFAULT_LOCAL_CONNECTION_STRING)


OUTPUT_FILE_LAM_PROPERTIES = pathlib.Path("custom_brick_v103_sample_graph.ttl").resolve()

rdf_graph = rdflib.Graph()
rdf_graph.parse(str(OUTPUT_FILE_LAM_PROPERTIES), format="ttl")

rdf2g.load_rdf2g(g, rdf_graph)
import pdb; pdb.set_trace()
rdf_type = "brick:Water_Distribution"

list_of_concept = rdf2g.get_nodes_of_type(g, rdf_type)

# print the list of concepts in the graph
print (list_of_concept)

node = rdf2g.get_node(g, "bldg:BUILDING")

tree = rdf2g.generate_traversal_tree(g, node)

result = rdf2g.expand_tree(g, tree)
pprint(result)
print("Chance to play with traversal tree...")
pdb.set_trace()

building_properties = rdf2g.get_node_properties(g, node)
# {'iri': 'https://example.com/customer_1/building_1#BUILDING', 'brick:TimeseriesUUID': 'UUID-1', '@label': 'bldg:BUILDING', '@id': 15}
print(building_properties)


edges_from_the_top = rdf2g.get_edges(g, building_properties.get('iri'), None)
print(len(edges_from_the_top))

rdf2g.get_node_properties(g, edges_from_the_top[-1].outV)

for edge in edges_from_the_top:
    pprint(edge)

edge = edges_from_the_top[0]
print(type(edge))
#<class 'gremlin_python.structure.graph.Edge'>

print(len(edges_from_the_top))
print(edge.id)
# 640
print(edge.label)
# 'brick:hasPart'
print(edge.inV.__dict__)
# {'id': 299, 'label': 'bldg:FLOOR_7'}
print(edge.inV.__dict__)
# {'id': 299, 'label': 'bldg:FLOOR_7'}

print("Chance to see edge properties")
pdb.set_trace()
