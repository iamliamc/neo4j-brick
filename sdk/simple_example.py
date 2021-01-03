from graph_connection import TopologyGraphDriver

neo4j_topology = TopologyGraphDriver(uri="neo4j://localhost:7687", password="", user="")

# Clean-up just to be sure...
neo4j_topology.destroy_graph()


neo4j_topology.initalize_neo4j_configuration()

load_ontology = True

# Run this if you want to load the BRICK Ontology alongside any specific BRICK schema implementation of a topology
if not neo4j_topology.is_brick_ontology_loaded() and load_ontology:
    neo4j_topology.load_brick_ontology()

# Load TTL from file system while running Neo4j in Docker requires setting up some shared directories therefore reference raw file on repo

# input_turtle = "https://raw.githubusercontent.com/iamliamc/neo4j-brick/main/examples/custom_brick_v11_sample_graph.ttl"

input_turtle = (
    "https://raw.githubusercontent.com/BrickSchema/Brick/master/examples/rice_brick.ttl"
)

neo4j_topology.load_ttl_file(input_turtle)

with neo4j_topology.driver.session() as session:
    results = session.run("MATCH (n:AHU)-[z]->(o) return n, z, o")
    ahus = [record["n"] for record in results]
    relationships = [record["z"] for record in results]
    related_nodes = [record["o"] for record in results]
    print(ahus, relationships, related_nodes)

import pdb

pdb.set_trace()

