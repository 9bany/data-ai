from typing import List
from db import Database, Table, Column
from sqlalchemy import Engine, text

class ClickHouseDatabase(Database):
    """
    ClickHouse-specific implementation of the abstract Database interface.
    This class provides methods to retrieve metadata about tables and columns
    from a ClickHouse database using SQLAlchemy.
    """

    def __init__(self, engine: Engine):
        # Initialize the database with a SQLAlchemy engine instance
        self.engine = engine

    def tables(self) -> List[Table]:
        """
        Retrieve a list of tables in the ClickHouse database.
        Returns a list of Table objects with basic metadata.
        """
        with self.engine.connect() as conn:
            # Execute SHOW TABLES to get all table names
            result = conn.execute(text("SHOW TABLES")).fetchall()
        return [Table(name=row[0], description="ClickHouse table") for row in result]

    def table(self, table_name: str) -> Table:
        """
        Retrieve metadata for a specific table in the ClickHouse database.
        Returns a Table object including its columns.
        """
        with self.engine.connect() as conn:
            # Use DESCRIBE TABLE to fetch column info
            result = conn.execute(text(f"DESCRIBE TABLE {table_name}")).fetchall()
        columns = [Column(name=row[0], type=row[1], description="") for row in result]
        return Table(name=table_name, description="ClickHouse table", columns=columns)

    def to_json(self) -> dict:
        """
        Serialize the entire database schema into a JSON-compatible dictionary.
        Includes all tables and their column definitions.
        """
        return {
            "database": "clickhouse",
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