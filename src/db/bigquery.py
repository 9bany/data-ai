from typing import List
from db import Database, Table, Column

class BigQueryDatabase(Database):
    """
    BigQuery-specific implementation of the abstract Database interface.
    This class provides methods to retrieve table and column metadata
    from a Google BigQuery dataset using the BigQuery client.
    """

    def __init__(self, client, dataset_id: str):
        """
        Initialize with a BigQuery client and the dataset ID.
        """
        # Store the BigQuery client and dataset identifier for later use
        self.client = client
        self.dataset_id = dataset_id

    def tables(self) -> List[Table]:
        """
        Retrieve a list of all tables in the specified BigQuery dataset.
        Returns a list of Table objects.
        """
        # List all tables in the dataset using the BigQuery client
        tables = self.client.list_tables(self.dataset_id)
        # For each table, retrieve full metadata using _get_table
        return [self._get_table(table.table_id) for table in tables]

    def table(self, table_name: str) -> Table:
        """
        Retrieve metadata for a specific table in the dataset.
        Returns a Table object with column metadata.
        """
        # Get metadata for a single table by name
        return self._get_table(table_name)

    def _get_table(self, table_name: str) -> Table:
        """
        Internal helper method to retrieve schema details for a specific table.
        Returns a Table object constructed from BigQuery schema fields.
        """
        # Construct the full BigQuery table reference
        table_ref = f"{self.dataset_id}.{table_name}"
        # Fetch the table metadata from BigQuery
        table = self.client.get_table(table_ref)
        # Convert each field in the table schema to a Column object
        columns = [
            Column(name=field.name, type=field.field_type, description=field.description or "")
            for field in table.schema
        ]
        # Return a Table object with the table's columns
        return Table(name=table.table_id, description="BigQuery table", columns=columns)

    def to_json(self) -> dict:
        """
        Serialize the BigQuery dataset schema to a JSON-compatible dictionary format.
        Includes all tables and their associated columns.
        """
        # Build a dictionary representing the dataset with all table and column metadata
        return {
            "database": self.dataset_id,
            "tables": [
                {
                    "name": table.name,
                    "description": table.description,
                    "columns": [
                        {
                            "name": col.name,
                            "type": col.type,
                            "description": col.description
                        } for col in table.columns
                    ]
                }
                for table in self.tables()
            ]
        }
    
