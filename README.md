See the most trivial example  in [sdk/simple_example.py](https://github.com/iamliamc/neo4j-brick/blob/main/sdk/simple_example.py)

How to launch the Neo4J instance on docker locally:
```
    docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --env='NEO4JLABS_PLUGINS=["apoc", "n10s"]' --env=NEO4J_AUTH=none neo4j:latest
```

Run it in detached mode
```
    docker run -d --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --env='NEO4JLABS_PLUGINS=["apoc", "n10s"]' --env=NEO4J_AUTH=none neo4j:latest

```

Connect to the Neo4j browser with the [Neo4j Desktop App](https://neo4j.com/download/) or by visiting `localhost:7474` 

This interesting query returns the ENTIRE sub-graph connected to Resource:Building
See the [APOC library](https://neo4j.com/labs/apoc/4.1/)
```
    MATCH (n:Resource:Building)
    CALL apoc.path.subgraphNodes(n, {minLevel:1}) YIELD node
    RETURN node
```

How to run tests:
```
    pytest -c pytest.ini tests
```