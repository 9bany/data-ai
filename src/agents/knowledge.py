import json
from sqlalchemy import Engine
from uuid import uuid4
from db.pg import PostgreSQLDatabase
from db.mysql import MySQLDatabase
from db.clickhouse import ClickHouseDatabase
from db import Database
from store import StoreDb
from agno.knowledge.json import JSONKnowledgeBase
from agno.document.base import Document
from agents import (
    get_structure_usage_explainer,
    get_structure_explainer_with_example,
    get_table_use_case_extractor,
)
from textwrap import dedent
from helper import agent_name as map_agent_name
from sqlalchemy import create_engine

# Determine which database implementation to use based on the SQLAlchemy engine driver
def db_knowledge(engine: Engine) -> Database:
    if engine.driver == "psycopg2":
        return PostgreSQLDatabase(engine=engine)
    if engine.driver == "pymysql":
        return MySQLDatabase(engine=engine)
    if engine.driver == "native":
        return ClickHouseDatabase(engine=engine)
    raise ValueError(f"Unsupported database driver: {engine.driver}")

# Delete vectorized knowledge associated with an agent
def drop_member_knowledge(agent_name: str):
    vector = StoreDb().knowleged_base_db(collection=agent_name)
    knowledge_base = JSONKnowledgeBase(vector_db=vector)
    knowledge_base.delete()

# Generate semantic descriptions and use cases for all tables in the database
def get_table_semantic(uri: str):
    try:
        engine = create_engine(url=uri)
        db = db_knowledge(engine=engine)
        response = get_table_use_case_extractor().run(json.dumps(db.to_json()))
        return response.content
    except Exception as e:
        raise ValueError(f"Failed to process database: {uri}: {e}")

# Extract structure-level knowledge and store it in the vector database for one agent
def process_member_knowledge(agent_name: str, knowledge: str):
    explainer = get_structure_explainer_with_example()
    response = explainer.run(message=knowledge)
    document = Document(
        name=agent_name,
        id=str(uuid4()),
        meta_data={"page": 0},
        content=response.content,
    )
    
    vector = StoreDb().knowleged_base_db(collection=agent_name)
    knowledge_base = JSONKnowledgeBase(vector_db=vector)
    knowledge_base.load_documents(documents=[document], upsert=True)

# Extract team-level understanding of database use case and store in team vector space
def process_team_knowledge(agent_name: str, knowledge: str) -> Document: 
    explainer = get_structure_usage_explainer()
    response = explainer.run(message=knowledge)

    document = Document(
        name=agent_name,
        id=str(uuid4()),
        meta_data={"page": 0},
        content=response.content,
    )

    StoreDb().data_team_knowledge.load_documents(documents=[document], upsert=True)

# End-to-end processing: load DB schema, generate knowledge, and store both member & team representations
def process_database(name: str, uri: str):
    agent_name = map_agent_name(name)
    try:
        engine = create_engine(url=uri)
        db = db_knowledge(engine=engine)
        process_member_knowledge(
            agent_name=agent_name, 
            knowledge=json.dumps(db.to_json()),
        )
        process_team_knowledge(
            agent_name=agent_name, 
            knowledge=json.dumps(db.to_json()),
        )
    except Exception as e:
        raise ValueError(f"Failed to process database: {name}: {e}")
