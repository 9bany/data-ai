"""
This module provides a singleton-based store for managing memory, app-level
database storage, and vectorized knowledge bases used by the Data-AI platform.
"""

from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from constants import (
    DB_MEM_FILE,
    DB_STORE_FILE,
    DB_VECTOR_FILE
)
from agno.vectordb.chroma import ChromaDb
from agno.agent import AgentKnowledge
from agno.knowledge.text import TextKnowledgeBase
from .app import DatabaseStore

# Singleton metaclass to ensure only one instance of StoreDb exists
class SingletonMem(type):
    """
    Singleton metaclass to ensure a class has only one instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
# Centralized access point for all memory, database, and knowledge base layers
class StoreDb(metaclass=SingletonMem):
    """
    Singleton store for managing:
    - User memory database
    - Application database metadata store
    - Vectorized knowledge for team-wide reasoning
    """

    def __init__(self) -> None:
        # Initialize memory for user interactions using local SQLite + OpenAI model
        memory = Memory(
            model=OpenAIChat(id="gpt-4.1"),
            db=SqliteMemoryDb(table_name="tb_user_memories", db_file=DB_MEM_FILE),
        )
        self.memory_db = memory

        # Initialize database metadata store (SQLite)
        self.app_store = DatabaseStore(db_path=DB_STORE_FILE)
        
        # Persistent vector DB for team-level shared knowledge base
        vector = ChromaDb(
            path=DB_VECTOR_FILE, 
            collection="data-team-knowledge_base", 
            persistent_client=True,
        )
        self.data_team_knowledge = TextKnowledgeBase(vector_db=vector)

    def knowleged_base_db(self, collection: str) -> AgentKnowledge:
        """
        Create or retrieve a knowledge base for a specific agent or collection.
        Uses Chroma vector DB for persistence.
        """
        return ChromaDb(
            path=DB_VECTOR_FILE, 
            collection=collection,
            persistent_client=True,
        )
