from typing import List
from sqlalchemy import text
from sqlalchemy.engine import Engine
from db import Database, Table, Column

class MySQLDatabase(Database):
    def __init__(self, engine: Engine):
        self.engine = engine

    def tables(self) -> List[Table]:
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    table_name,
                    table_comment
                FROM
                    information_schema.tables
                WHERE
                    table_schema = DATABASE()
            """))
            table_rows = result.fetchall()

            tables = []
            for table_name, table_comment in table_rows:
                tables.append(self._get_table(conn, table_name, table_comment))
            return tables

    def table(self, table_name: str) -> Table:
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT
                    table_comment
                FROM
                    information_schema.tables
                WHERE
                    table_schema = DATABASE()
                    AND table_name = :table_name
            """), {"table_name": table_name})
            row = result.fetchone()
            if not row:
                raise ValueError(f"Table '{table_name}' not found.")
            return self._get_table(conn, table_name, row[0])

    def _get_table(self, conn, table_name: str, table_description: str) -> Table:
        result = conn.execute(text("""
            SELECT
                column_name,
                data_type,
                column_comment
            FROM
                information_schema.columns
            WHERE
                table_schema = DATABASE()
                AND table_name = :table_name
            ORDER BY
                ordinal_position
        """), {"table_name": table_name})
        columns = [
            Column(name, type_, desc or "")
            for name, type_, desc in result.fetchall()
        ]
        return Table(name=table_name, description=table_description or "", columns=columns)

    def to_json(self) -> dict:
        """Return the database metadata as a JSON-serializable dictionary."""
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
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