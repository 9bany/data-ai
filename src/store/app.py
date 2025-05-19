import sqlite3
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class DatabaseObject:
    id: int
    name: str
    uri: str
    driver: str
    meta_data: str

class DatabaseStore:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS databases (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                driver TEXT NOT NULL,
                uri TEXT NOT NULL,
                meta_data TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create(self, db_entry: Dict):
        self.conn.execute(
            "INSERT INTO databases (name, driver, uri, meta_data) VALUES (?, ?, ?, ?)",
            (db_entry["name"], db_entry["driver"], db_entry["uri"], db_entry["meta_data"])
        )
        self.conn.commit()

    def get_all(self) -> List[DatabaseObject]:
        cursor = self.conn.execute("SELECT id, name, uri, driver, meta_data FROM databases")
        return [
            DatabaseObject(id=row[0], name=row[1], uri=row[2], driver=row[3], meta_data=row[4])
            for row in cursor.fetchall()
        ]
    def delete(self, name: str) -> List[DatabaseObject]:
        self.conn.execute("DELETE FROM databases WHERE name = ?", (name,))
        self.conn.commit()