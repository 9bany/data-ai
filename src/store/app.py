"""
This module provides a simple SQLite-based persistence layer for storing and managing
database connection metadata used by the Data-AI platform.
"""

import sqlite3
from typing import List, Dict
from dataclasses import dataclass

# Represents a structured object holding metadata about a registered database
@dataclass
class DatabaseObject:
    id: int
    name: str
    uri: str
    driver: str
    meta_data: str

# Class for managing storage of database connection metadata using SQLite
class DatabaseStore:
    def __init__(self, db_path: str):
        """
        Initialize the SQLite connection and ensure the table exists.
        """
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        """
        Create the 'databases' table if it doesn't exist.
        The table stores: ID, name, driver, URI, and associated metadata.
        """
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
        """
        Insert a new database entry into the table if the URI is not already present.
        This prevents duplicate entries based on the URI field.
        """
        # Check if a database with the same URI already exists
        cursor = self.conn.execute(
            "SELECT COUNT(*) FROM databases WHERE uri = ?",
            (db_entry["uri"],)
        )
        if cursor.fetchone()[0] > 0:
            return  # Skip creation if URI already exists

        # Insert the new database entry
        self.conn.execute(
            "INSERT INTO databases (name, driver, uri, meta_data) VALUES (?, ?, ?, ?)",
            (db_entry["name"], db_entry["driver"], db_entry["uri"], db_entry["meta_data"])
        )
        self.conn.commit()

    def get_all(self) -> List[DatabaseObject]:
        """
        Retrieve all database records as a list of DatabaseObject instances.
        """
        # Query all database entries
        cursor = self.conn.execute("SELECT id, name, uri, driver, meta_data FROM databases")
        return [
            DatabaseObject(id=row[0], name=row[1], uri=row[2], driver=row[3], meta_data=row[4])
            for row in cursor.fetchall()
        ]

    def delete(self, name: str) -> List[DatabaseObject]:
        """
        Delete a database entry from the table based on its name.
        """
        # Delete the database entry with the specified name
        self.conn.execute("DELETE FROM databases WHERE name = ?", (name,))
        self.conn.commit()