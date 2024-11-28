from neo4j import GraphDatabase



# חיבור ל-Neo4j
def init_neo4j():
    return GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "password")
    )
