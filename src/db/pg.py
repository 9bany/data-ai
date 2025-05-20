from typing import List
from sqlalchemy import text
from sqlalchemy.engine import Engine
from db import Database, Table, Column

class PostgreSQLDatabase(Database):
    """
    PostgreSQL-specific implementation of the abstract Database interface.
    This class provides methods to retrieve metadata about tables and columns
    from a PostgreSQL database using SQLAlchemy.
    """

    def __init__(self, engine: Engine):
        # Initialize with a SQLAlchemy engine to connect to the PostgreSQL database
        self.engine = engine

    def tables(self) -> List[Table]:
        """
        Retrieve all user-defined tables in the public schema of the database.
        Returns a list of Table objects with basic metadata.
        """
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    c.relname AS table_name,
                    obj_description(c.oid) AS table_description
                FROM
                    pg_class c
                JOIN
                    pg_namespace n ON n.oid = c.relnamespace
                WHERE
                    c.relkind = 'r'
                    AND n.nspname = 'public'
            """))
            table_rows = result.fetchall()

            tables = []
            for table_name, table_desc in table_rows:
                tables.append(self._get_table(conn, table_name, table_desc))
            return tables

    def table(self, table_name: str) -> Table:
        """
        Retrieve metadata for a specific table in the public schema.
        Returns a Table object if found, otherwise raises an error.
        """
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    obj_description(c.oid) AS table_description
                FROM
                    pg_class c
                JOIN
                    pg_namespace n ON n.oid = c.relnamespace
                WHERE
                    c.relname = :table_name
                    AND n.nspname = 'public'
                    AND c.relkind = 'r'
            """), {"table_name": table_name})
            row = result.fetchone()
            if not row:
                raise ValueError(f"Table '{table_name}' not found.")
            return self._get_table(conn, table_name, row[0])

    def _get_table(self, conn, table_name: str, table_description: str) -> Table:
        """
        Internal helper method to fetch column metadata for a given table name.
        Returns a Table object with a list of associated Column objects.
        """
        result = conn.execute(text("""
            SELECT
                cols.column_name,
                cols.data_type,
                pgd.description
            FROM
                information_schema.columns cols
            LEFT JOIN
                pg_catalog.pg_statio_all_tables st ON cols.table_schema = st.schemaname AND cols.table_name = st.relname
            LEFT JOIN
                pg_catalog.pg_description pgd ON pgd.objoid = st.relid AND pgd.objsubid = cols.ordinal_position
            WHERE
                cols.table_schema = 'public'
                AND cols.table_name = :table_name
            ORDER BY
                cols.ordinal_position
        """), {"table_name": table_name})
        columns = [
            Column(name, type_, desc or "")
            for name, type_, desc in result.fetchall()
        ]
        return Table(name=table_name, description=table_description or "", columns=columns)

    def to_json(self) -> dict:
        """
        Convert the entire database schema (tables and columns) into a JSON-serializable dictionary.
        """
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.scalar()

        return {
            "database": db_name,
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