from typing import List
from db import Database, Table

class MongoDatabase(Database):
    def __init__(self, client):
        self.client = client

    def tables(self) -> List[Table]:
        db = self.client.get_default_database()
        return [Table(name=col, description="MongoDB collection") for col in db.list_collection_names()]

    def table(self, table_name: str) -> Table:
        return Table(name=table_name, description="MongoDB collection")

    def to_json(self) -> dict:
        db = self.client.get_default_database()
        return {
            "database": db.name,
            "tables": [
                {
                    "name": col,
                    "description": "MongoDB collection",
                    "columns": []
                }
                for col in db.list_collection_names()
            ]
        }
