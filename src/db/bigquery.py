from typing import List
from db import Database, Table, Column

class BigQueryDatabase(Database):
    def __init__(self, client, dataset_id: str):
        self.client = client
        self.dataset_id = dataset_id

    def tables(self) -> List[Table]:
        tables = self.client.list_tables(self.dataset_id)
        return [self._get_table(table.table_id) for table in tables]

    def table(self, table_name: str) -> Table:
        return self._get_table(table_name)

    def _get_table(self, table_name: str) -> Table:
        table_ref = f"{self.dataset_id}.{table_name}"
        table = self.client.get_table(table_ref)
        columns = [
            Column(name=field.name, type=field.field_type, description=field.description or "")
            for field in table.schema
        ]
        return Table(name=table.table_id, description="BigQuery table", columns=columns)

    def to_json(self) -> dict:
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
    
