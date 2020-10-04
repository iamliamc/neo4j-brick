import pdb
import py2neo
from neo4j import GraphDatabase
import logging


class TopologyGraphDriver:
    """
        Based on: https://neo4j.com/docs/driver-manual/current/get-started/#driver-get-started-hello-world-example
    """

    brick_version = "1.1"
    default_uri = "neo4j://localhost:7687"
    logger = logging.getLogger()

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_brick_ontology(self):
        with self.driver.session() as session:
            session.run(self._load_brick_ontology)

    def is_brick_ontology_loaded(self):
        with self.driver.session() as session:
            is_brick_loaded = session.read_transaction(self._is_brick_ontology_loaded)
            # TODO is there a better mechanism to validate this?
            if len(is_brick_loaded) > 0:
                return True
            else:
                return False

    def enable_neosemantics_for_neo4j(self):
        with self.driver.session() as session:
            graph_config = session.call(self._configure_graph)


    def destroy_graph(self, require_cli_input=True):
        if require_cli_input:
            self.logger.info("Requesting CLI confirmation of delete graph")
            value = input("Are you sure you want to delete everything from the graph? y/n")
            if value != "y":
                self.logger.info(f"Responded {value} skipping TopologyGraphDriver.destroy_graph call")
                return 

        self.logger.info(f"Deleting all graph entities...")
        with self.driver.session() as session:
            results = session.run(self._destroy_graph)
            return results
    
    @staticmethod
    def _load_neosemantics_plugin_and_configure_graph():
        pass

    @staticmethod
    def _destroy_graph(tx):
        results = tx.run('MATCH (n) DETACH DELETE n')
        return results

    @staticmethod
    def _get_brick_relationships(tx):
        results = tx.run('MATCH(n:Resource:Relationship where n.uri CONTAINS "https://brickschema.org/schema/1.1/Brick#" RETURN n')
        return [record["n"] for record in results]

    @staticmethod
    def _get_brick_classes(tx):
        results = tx.run('MATCH(n:Resource:Class where n.uri CONTAINS "https://brickschema.org/schema/1.1/Brick#" RETURN n')
        return [record["n"] for record in results]

    @staticmethod
    def _is_brick_ontology_loaded(tx):
        results = tx.run('MATCH(n:Resource) where n.uri CONTAINS "https://brickschema.org/schema/1.1/Brick#" RETURN n LIMIT 10')
        return [record["n"] for record in results]

    @staticmethod
    def _load_brick_ontology(tx):
        results = tx.run('CALL n10s.onto.import.fetch("https://brickschema.org/schema/1.1/Brick.ttl", "Turtle");')
        return results

    @staticmethod
    def _create_neosemantics_constraint(tx):
        results = tx.run('CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE')
        pdb.set_trace()
        return results

    @staticmethod
    def _

    @staticmethod
    def _drop_graph_config(tx):
        results = tx.run('CALL n10s.graphconfig.drop')
        return results
