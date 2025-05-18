import typer
import json
from typing import List
from sqlalchemy import Engine
from rich.table import Table
from rich.console import Console
from uuid import uuid4

from agents.agent import get_sql_agent
from db.pg import PostgreSQLDatabase
from db import Database
from store import StoreDb
from agno.utils.log import logger

databases = StoreDb().app_store.read_all()

from agno.agent import Agent
from agno.knowledge.json import JSONKnowledgeBase
from agno.document.base import Document
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from constants import USER_ID

def load_db_knowledge(engine: Engine) -> Database:
    if engine.driver == "psycopg2":
        return PostgreSQLDatabase(engine=engine)
    raise ValueError(f"Unsupported database driver: {engine.driver}")

list_agents: List[Agent] = []

def init_team():
    for el in databases:
        from sqlalchemy import create_engine
        try:
            engine = create_engine(url=el.uri)
            db = load_db_knowledge(engine=engine)

            document = Document(
                name=el.name,
                id=str(uuid4()),
                meta_data={"page": 0},
                content=json.dumps(db.to_json()),
            )
            
            collection = f"agent-{el.name}"
            logger.info(f"Loading {collection} knowledge.")

            vector = StoreDb().knowleged_base_db(collection=collection)
            knowledge_base = JSONKnowledgeBase(
                vector_db=vector)
            knowledge_base.load_documents(documents=[document], upsert=True)
            
            logger.info(f"{collection} knowledge loaded.")

            agent = get_sql_agent(db_engine=engine, knowledge_base=knowledge_base)
            list_agents.append(agent)
        except Exception as e:
            typer.echo(f"Failed to load agent for {el.name}: {e}")
            exit(0)

    if not list_agents:
        typer.echo("No valid agents found. Exiting.")
        return

    agent_team = Team(
        name="Data Team",
        mode="coordinate",
        model=OpenAIChat("gpt-4o"),
        memory=StoreDb().memory_db,
        enable_user_memories=True,
        enable_agentic_memory=True,
        markdown=True,
        num_history_runs=50,
        members=list_agents,
        instructions=[
            "You are the team leader responsible for managing a group of database agents.",
            "Each agent represents knowledge extracted from a different data source (PostgreSQL, MySQL, MongoDB, etc.).",
            "Your role is to coordinate the discussion, ask clarifying questions, and summarize responses from agents.",
            "You must detect when the team has reached consensus, or when conflicting opinions exist.",
            "Encourage collaboration, but ensure the team stays on topic and works toward the success criteria.",
            "Use markdown formatting when giving final outputs or summaries.",
            "You can delegate sub-tasks to specific agents, but always guide the conversation back to the main goal.",
            "If the discussion stalls or diverges, bring it back to the key objective using your knowledge of the task.",
        ],
        success_criteria="The team has reached a consensus.",
        enable_agentic_context=True,
        show_members_responses=True,
        show_tool_calls=False,
        user_id=USER_ID,
    )
    return agent_team

team_leader = init_team()