import sqlite3
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class DatabaseObject:
    id: int
    name: str
    uri: str
    driver: str

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
                uri TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create(self, db_entry: Dict):
        self.conn.execute(
            "INSERT INTO databases (name, driver, uri) VALUES (?, ?, ?)",
            (db_entry["name"], db_entry["driver"], db_entry["uri"])
        )
        self.conn.commit()

    def read_all(self) -> List[DatabaseObject]:
        cursor = self.conn.execute("SELECT id, name, uri, driver FROM databases")
        return [
            DatabaseObject(id=row[0], name=row[1], uri=row[2], driver=row[3])
            for row in cursor.fetchall()
        ]