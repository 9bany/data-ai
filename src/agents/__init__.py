"""
This module exposes key agent constructors for database understanding and explanation.

Each function returns an Agent configured for a specific use case:
- When and why to use a database structure
- Providing example queries for a schema
- Describing use cases for each table in a database
"""

from agents.base import (
    get_structure_usage_explainer,           # Explains when to use a DB structure
    get_structure_explainer_with_example,    # Explains structure + provides query examples
    get_table_use_case_extractor,            # Extracts table use cases in structured format
)

__all__ = [
    "get_structure_usage_explainer",
    "get_structure_explainer_with_example",
    "get_table_use_case_extractor",
]