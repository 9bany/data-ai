
import os
from os.path import join, dirname
from config import Config

dotenv_path = join(dirname(dirname(__file__)), ".env")
os.environ["PROJECT_DIR"] = dirname(dirname(__file__))
Config(env_file=dotenv_path, data_injection={"any": "yes"})

import uuid
import os
import typer
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

app = typer.Typer()
user_id = "root"

def supported_driver(driver: str) -> bool:
    if driver == "psycopg2":
        return True
    raise False

def load_db_knowledge(engine: Engine) -> Database:
    if engine.driver == "psycopg2":
        return PostgreSQLDatabase(engine=engine)
    raise ValueError(f"Unsupported database driver: {engine.driver}")

@app.command()
def add(uri: str, name: str = typer.Option(None)):
    from sqlalchemy import create_engine
    try:
        engine = create_engine(url=uri)
        if supported_driver(driver=engine.driver):
            name = name or f"db-{uuid.uuid4().hex[:6]}"
            StoreDb().app_store.create({
                "name": name,
                "uri": uri,
                "driver": engine.driver
            })
            console = Console()
            table = Table(title="Database Added", show_lines=True)
            table.add_column("Name", style="cyan")
            table.add_column("Driver", style="green")
            table.add_column("URI", style="magenta")
            table.add_row(name, engine.driver, uri)
            console.print(table)
        else: 
            typer.echo(f"Unsupported driver: {engine.driver}")
    except Exception as e:
        typer.echo(f"Failed {e}")

@app.command()
def list():
    console = Console()
    table = Table(title="Database List")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Driver", style="green")
    table.add_column("URI", style="yellow")
    for db in StoreDb().app_store.read_all():
        table.add_row(
            str(db.id),
            db.name,
            db.driver,
            db.uri
        )
    console.print(table)

@app.command()
def chat():
    
    databases = StoreDb().app_store.read_all()
    
    from agno.agent import Agent
    from agno.knowledge.json import JSONKnowledgeBase
    from agno.document.reader.json_reader import JSONReader 
    from agno.document.base import Document
    from agno.models.openai import OpenAIChat
    from agno.team.team import Team
    import json
    
    list_agents: List[Agent] = []
    
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
            "You are a discussion master.",
            "You have to stop the discussion when you think the team has reached a consensus.",
        ],
        success_criteria="The team has reached a consensus.",
        enable_agentic_context=True,
        show_members_responses=True,
        show_tool_calls=False,
        user_id=user_id,
    )

    agent_team.cli_app()

def main():
    app()

if __name__ == "__main__":
    main()
