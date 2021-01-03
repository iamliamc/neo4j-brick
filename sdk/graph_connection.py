import pdb
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ClientError as neo4jException


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
            session.write_transaction(self._load_brick_ontology)

    def is_brick_ontology_loaded(self):
        with self.driver.session() as session:
            is_brick_loaded = session.read_transaction(self._is_brick_ontology_loaded)
            # TODO is there a better mechanism to validate this?
            if len(is_brick_loaded) > 0:
                return True
            else:
                return False

    def get_brick_classes(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_brick_classes)

    def get_brick_relationships(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_brick_relationships)

    def destroy_graph(self, require_cli_input=True):
        if require_cli_input:
            self.logger.info("Requesting CLI confirmation of delete graph")
            value = input(
                "Are you sure you want to delete everything from the graph? y/n"
            )
            if value != "y":
                self.logger.info(
                    f"Responded {value} skipping TopologyGraphDriver.destroy_graph call"
                )
                return

        self.logger.info(f"Deleting all graph entities...")
        with self.driver.session() as session:
            results = session.write_transaction(self._destroy_graph)
            return results

    def initalize_neo4j_configuration(self):
        enable_neosemantics = None
        configure_graph = None

        try:
            with self.driver.session() as session:
                enable_neosemantics = session.write_transaction(
                    self._create_neosemantics_constraint
                )
        except neo4jException as e:
            if e.title == "EquivalentSchemaRuleAlreadyExists":
                self.logger.info(f"Neosemantics Schema Rule Already Exists...")
            else:
                self.logger.error(e)

        try:
            with self.driver.session() as session:
                configure_graph = session.write_transaction(self._create_graph_config)
        except neo4jException as e:
            self.logger.info(e.message)

        return enable_neosemantics, configure_graph

    def load_ttl_file(self, filepath: str):
        with self.driver.session() as session:
            return session.write_transaction(self._load_ttl_file, filepath)

    @staticmethod
    def _destroy_graph(tx):
        results = tx.run("MATCH (n) DETACH DELETE n")
        return results

    @staticmethod
    def _get_brick_relationships(tx):
        results = tx.run(
            'MATCH(n:Resource:Relationship) WHERE n.uri CONTAINS "https://brickschema.org/schema/1.1/Brick#" RETURN n'
        )
        return [record["n"] for record in results]

    @staticmethod
    def _get_brick_classes(tx):
        results = tx.run(
            'MATCH(n:Resource:Class) WHERE n.uri CONTAINS "https://brickschema.org/schema/1.1/Brick#" RETURN n'
        )
        return [record["n"] for record in results]

    @staticmethod
    def _is_brick_ontology_loaded(tx):
        results = tx.run(
            'MATCH(n:Resource) where n.uri CONTAINS "https://brickschema.org/schema/1.1/Brick#" RETURN n LIMIT 10'
        )
        return [record["n"] for record in results]

    @staticmethod
    def _load_brick_ontology(tx):
        results = tx.run(
            'CALL n10s.onto.import.fetch("https://brickschema.org/schema/1.1/Brick.ttl", "Turtle");'
        )
        return results

    @staticmethod
    def _create_neosemantics_constraint(tx):
        results = tx.run(
            "CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE"
        )
        return results

    @staticmethod
    def _create_graph_config(tx):
        results = tx.run("CALL n10s.graphconfig.init({handleVocabUris: 'IGNORE'})")
        return results

    @staticmethod
    def _drop_graph_config(tx):
        results = tx.run("CALL n10s.graphconfig.drop")
        return results

    @staticmethod
    def _load_ttl_file(tx, filepath: str):
        # Any sources on github make sure to use the raw file:
        # https://raw.githubusercontent.com/BrickSchema/Brick/master/examples/rice_brick.ttl
        # TODO deal with verifyUriSyntax

        results = tx.run(
            f'CALL n10s.rdf.import.fetch("{filepath}", "Turtle", {{verifyUriSyntax: false}})'
        )

        return results
