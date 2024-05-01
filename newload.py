import csv
import requests
from neo4j import GraphDatabase
from typing import Dict, Any
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Neo4jAuraLoader:
    """Handles connection to Neo4j Aura and loading data into the database."""

    def __init__(self, uri: str, user: str, password: str):
        """
        Initializes Neo4jAuraLoader with connection details.

        Args:
            uri (str): Neo4j Aura database URI.
            user (str): Neo4j Aura username.
            password (str): Neo4j Aura password.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        """Cleanup method to close the Neo4j driver."""
        if self.driver:
            self.driver.close()

    def insert_data(self, cypher_query: str, parameters: Dict[str, Any]):
        """
        Inserts data into Neo4j Aura database.

        Args:
            cypher_query (str): Cypher query template.
            parameters (dict): Parameters for the Cypher query.
        """
        with self.driver.session() as neo4j_session:
            neo4j_session.run(cypher_query, parameters)


class CSVLoader:
    """Handles downloading and processing CSV data."""

    def __init__(self, csv_url: str):
        """
        Initializes CSVLoader with the CSV file URL.

        Args:
            csv_url (str): URL of the CSV file.
        """
        self.csv_url = csv_url

    def download_csv(self) -> str:
        """Downloads CSV data and returns the content."""
        with requests.Session() as session:
            with session.get(self.csv_url) as response:
                response.raise_for_status()
                return response.text

    def process_csv(self, csv_text: str, limit: int, neo4j_loader: Neo4jAuraLoader, cypher_query: str) -> None:
        """
        Processes CSV data and inserts it into Neo4j Aura database.

        Args:
            csv_text (str): Text content of the CSV file.
            limit (int): Limit for rows to be processed.
            neo4j_loader (Neo4jAuraLoader): Instance of Neo4jAuraLoader for data insertion.
            cypher_query (str): Cypher query template.
        """
        csvreader = csv.DictReader(csv_text.splitlines(), delimiter=',', quotechar='"')
        count = 0
        for row in csvreader:
            if count >= limit:
                break

            parameters = {
                'year': int(row['year']),
                'make': row['make'],
                'model': row['model'],
                'trim': row['trim'],
                'body': row['body'],
                'transmission': row['transmission'],
                'vin': row['vin'],
                'state': row['state'],
                'condition': row['condition'],
                'odometer': int(row['odometer']) if row['odometer'] else None,
                'color': row['color'],
                'interior': row['interior'],
                'seller': row['seller'],
                'mmr': float(row['mmr']),
                'sellingprice': float(row['sellingprice']),
                'saledate': row['saledate']
            }

            neo4j_loader.insert_data(cypher_query, parameters)
            count += 1


if __name__ == "__main__":
    # Cypher query template
    cypher_query = """
        CREATE (:Car {
            year: $year,
            make: $make,
            model: $model,
            trim: $trim,
            body: $body,
            transmission: $transmission,
            vin: $vin,
            state: $state,
            condition: $condition,
            odometer: $odometer,
            color: $color,
            interior: $interior,
            seller: $seller,
            mmr: $mmr,
            sellingprice: $sellingprice,
            saledate: $saledate
        })
    """

    # CSV file URL
    csv_url = "https://raw.githubusercontent.com/pachav99/Final-Project-Big-Data/master/Vehicle_prices.csv"

    # Limit for rows to be processed
    limit = 70000

    # Initialize Neo4jAuraLoader
    neo4j_loader = Neo4jAuraLoader(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # Initialize CSVLoader
    csv_loader = CSVLoader(csv_url)

    # Download CSV data
    csv_text = csv_loader.download_csv()

    # Process CSV data and insert into Neo4j Aura
    csv_loader.process_csv(csv_text, limit, neo4j_loader, cypher_query)

    print("Data loaded into Neo4j Aura instance.")
