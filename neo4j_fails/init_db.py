from neo4j import GraphDatabase



# חיבור ל-Neo4j
def init_neo4j():
    return GraphDatabase.driver(
        "bolt://neo4j_fails:7687",
        auth=("neo4j_fails", "password")
    )
