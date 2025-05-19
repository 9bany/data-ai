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

class SingletonMem(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class StoreDb(metaclass=SingletonMem):

    def __init__(self) -> None:

        memory = Memory(
            model=OpenAIChat(id="gpt-4.1"),
            db=SqliteMemoryDb(table_name="tb_user_memories", db_file=DB_MEM_FILE),
        )
        self.memory_db = memory
        self.app_store = DatabaseStore(db_path=DB_STORE_FILE)
        
        vector = ChromaDb(path=DB_VECTOR_FILE, collection="data-team-knowledge_base")
        self.data_team_knowledge = TextKnowledgeBase(vector_db=vector)

    def knowleged_base_db(self, collection: str)-> AgentKnowledge:
        return ChromaDb(
            path=DB_VECTOR_FILE, 
            collection=collection,
            persistent_client=True,
        )
