from neo4j import GraphDatabase
import pandas as pd
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

def retrieve_data_from_neo4j(cypher_query: str) -> pd.DataFrame:
    """
    Retrieves data from Neo4j database.

    Args:
        cypher_query (str): Cypher query to execute.

    Returns:
        pd.DataFrame: DataFrame containing the retrieved data.
    """
    # Establish connection to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        # Retrieve data from Neo4j
        with driver.session() as session:
            result = session.run(cypher_query)
            records = [record.values() for record in result]

        # Convert data into a DataFrame
        df = pd.DataFrame(records, columns=result.keys())

        return df
    finally:
        # Close the Neo4j driver
        if driver:
            driver.close()

# Example usage:
if __name__ == "__main__":
    cypher_query = "MATCH (n:Person) RETURN n.name AS Name, n.age AS Age LIMIT 10"
    df = retrieve_data_from_neo4j(cypher_query)

    # Define the Cypher query
cypher_query = """
    MATCH (c:Car)
    RETURN c.year AS year, c.make AS make, c.model AS model, c.trim AS trim,
           c.body AS body, c.transmission AS transmission, c.vin AS vin,
           c.state AS state, c.condition AS condition, c.odometer AS odometer,
           c.color AS color, c.interior AS interior, c.seller AS seller,
           c.mmr AS mmr, c.sellingprice AS sellingprice, c.saledate AS saledate
"""

# Retrieve data from Neo4j
df = retrieve_data_from_neo4j(cypher_query)




    
