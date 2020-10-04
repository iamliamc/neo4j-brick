How to launch the Neo4J instance on docker locally:
```
    docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --env='NEO4JLABS_PLUGINS=["apoc", "n10s"]' --env=NEO4J_AUTH=none neo4j:latest
```

How to run tests:
```
    pytest -c pytest.ini tests
```