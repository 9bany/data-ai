"""
This module defines abstract data structures and interfaces used to describe
and extract metadata from relational databases. It includes representations
for database columns, tables, and an abstract Database interface that other
database implementations must inherit from.
"""

from abc import ABC, abstractmethod
from typing import List

class Column:
    """
    A class representing a column in a database table.

    Attributes:
        name (str): The name of the column.
        type (str): The data type of the column.
        description (str): An optional description of the column.
    """
    def __init__(self, name: str, type: str, description: str = ""):
        self.name = name  # Name of the column
        self.type = type  # Data type of the column (e.g., int, text)
        self.description = description  # Optional description of the column

    def __repr__(self):
        return f"Column(name={self.name}, type={self.type}, description={self.description})"

class Table:
    """
    A class representing a table in a database.

    Attributes:
        name (str): The name of the table.
        description (str): An optional description of the table.
        columns (List[Column]): A list of columns belonging to the table.
    """
    def __init__(self, name: str, description: str = "", columns: List['Column'] = None):
        self.name = name  # Name of the table
        self.description = description  # Optional description of the table
        self.columns = columns or []  # List of Column objects

    def __repr__(self):
        return f"Table(name={self.name}, description={self.description}, columns={self.columns})"

class Database(ABC):
    """
    Abstract interface for accessing and describing a database.

    Implementations must define how to return a list of tables,
    retrieve a specific table, and export metadata as JSON.
    """
    @abstractmethod
    def tables(self) -> List[Table]:
        """Return a list of Table instances representing all tables in the database."""
        pass

    @abstractmethod
    def table(self, table_name: str) -> Table:
        """Return a Table instance for a given table name."""
        pass

    @abstractmethod
    def to_json(self) -> dict:
        """Return the database metadata in JSON-serializable format."""
        pass
