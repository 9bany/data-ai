from typing import List
from db import Database, Table

class MongoDatabase(Database):
    def __init__(self, client):
        self.client = client

    def tables(self) -> List[Table]:
        db = self.client.get_default_database()
        schema = db["__schema"]
        tables = []
        for col in db.list_collection_names():
            meta = schema.find_one({"collection": col}) or {}
            description = meta.get("table_info", "MongoDB collection")
            columns = meta.get("fields", {})
            tables.append(Table(
                name=col,
                description=description,
                columns=[{"name": k, "description": v} for k, v in columns.items()]
            ))
        return tables

    def table(self, table_name: str) -> Table:
        db = self.client.get_default_database()
        schema = db["__schema"]
        meta = schema.find_one({"collection": table_name}) or {}
        description = meta.get("table_info", "MongoDB collection")
        columns = meta.get("fields", {})
        return Table(
            name=table_name,
            description=description,
            columns=[{"name": k, "description": v} for k, v in columns.items()]
        )

    def to_json(self) -> dict:
        db = self.client.get_default_database()
        schema = db["__schema"]
        return {
            "database": db.name,
            "tables": [
                {
                    "name": col,
                    "description": (meta := schema.find_one({"collection": col}) or {}).get("table_info", "MongoDB collection"),
                    "columns": [{"name": k, "description": v} for k, v in meta.get("fields", {}).items()]
                }
                for col in db.list_collection_names()
            ]
        }
