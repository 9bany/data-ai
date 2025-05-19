from typing import List
from db import Database, Table, Column
from sqlalchemy import Engine, text
class ClickHouseDatabase(Database):
    def __init__(self, engine: Engine):
        self.engine = engine

    def tables(self) -> List[Table]:
        with self.engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES")).fetchall()
        return [Table(name=row[0], description="ClickHouse table") for row in result]

    def table(self, table_name: str) -> Table:
        with self.engine.connect() as conn:
            result = conn.execute(text(f"DESCRIBE TABLE {table_name}")).fetchall()
        columns = [Column(name=row[0], type=row[1], description="") for row in result]
        return Table(name=table_name, description="ClickHouse table", columns=columns)

    def to_json(self) -> dict:
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