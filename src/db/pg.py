from typing import List
from sqlalchemy import text
from sqlalchemy.engine import Engine
from db import Database, Table, Column

class PostgreSQLDatabase(Database):
    def __init__(self, engine: Engine):
        self.engine = engine

    def tables(self) -> List[Table]:
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
        """Return the database metadata as a JSON-serializable dictionary."""
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