from abc import ABC, abstractmethod
from typing import List

class Column:
    def __init__(self, name: str, type: str, description: str = ""):
        self.name = name
        self.type = type
        self.description = description

    def __repr__(self):
        return f"Column(name={self.name}, type={self.type}, description={self.description})"

class Table:
    def __init__(self, name: str, description: str = "", columns: List['Column'] = None):
        self.name = name
        self.description = description
        self.columns = columns or []

    def __repr__(self):
        return f"Table(name={self.name}, description={self.description}, columns={self.columns})"

class Database(ABC):
    @abstractmethod
    def tables(self) -> List[Table]:
        """Return a list of Table instances."""
        pass

    @abstractmethod
    def table(self, table_name: str) -> Table:
        """Return a Table instance by name."""
        pass
    @abstractmethod
    def to_json(self) -> dict:
        """Return a Json data"""
        pass
