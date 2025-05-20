import os
from os.path import join, dirname
from config import Config

dotenv_path = join(dirname(dirname(__file__)), ".env")
os.environ["PROJECT_DIR"] = dirname(dirname(__file__))
Config(env_file=dotenv_path, data_injection={"any": "yes"})

import typer
from rich.table import Table
from rich.console import Console
from store import StoreDb
from helper import (
    gen_hash_name,
    with_spinner, 
    agent_name,
    supported_driver,
)
from agno.utils.log import logger
from agents.knowledge import (
    process_database, 
    drop_member_knowledge,
    get_table_semantic,
)

logger.setLevel(Config().app_config.log_level)

app = typer.Typer(add_completion=False)

@app.command()
def delete(name: str):
    def delete():
        StoreDb().app_store.delete(name=name)
        drop_member_knowledge(agent_name=agent_name(name))
    with_spinner(f"Delete agent: {name}", delete)

@app.command()
def add(uri: str, name: str = typer.Option(None)):
    from sqlalchemy import create_engine
    try:
        engine = create_engine(url=uri)
        if supported_driver(driver=engine.driver) == True:
            name = name or gen_hash_name()
            meta_data = None
            def analyze_db():
                nonlocal meta_data
                process_database(name=name, uri=uri)
                meta_data = get_table_semantic(uri=uri)
            with_spinner("Analyze & load database knowledge", analyze_db)
            StoreDb().app_store.create({
                "name": name,
                "uri": uri,
                "driver": engine.driver,
                "meta_data": meta_data,
            })
            console = Console()
            table = Table(show_lines=True)
            table.add_column("Name", style="cyan")
            table.add_column("Driver", style="green")
            table.add_column("URI", style="magenta")
            table.add_row(name, engine.driver, uri)
            console.print(table)
        else: 
            typer.echo(f"Unsupported driver: {engine.driver}")
    except Exception as e:
        typer.echo(f"ERROR: {e}")

@app.command()
def list():
    console = Console()
    table = Table()
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Driver", style="green")
    table.add_column("URI", style="yellow")
    for db in StoreDb().app_store.get_all():
        table.add_row(
            str(db.id),
            db.name,
            db.driver,
            db.uri
        )
    console.print(table)

@app.command()
def chat(work_mode: str = "route", show_member_response: bool = False):
    """
    Start a team-based conversation with AI agents that represent different databases.

    Parameters:
    - work_mode (str): Select team behavior mode. Options:
        - "route": Only one best-matched agent will respond to the user's question.
        - "coordinate": Multiple agents will contribute to the final answer by reasoning together. This mode allows collaborative problem solving when information is distributed across agents.

    - show_member_response (bool): If True, shows each agent's individual response before the final synthesized output.

    Example:
        To answer a question like "Get recent transactions for user ID 5" where:
        - MySQL agent holds user and order tables
        - Postgres agent holds transaction table

        The coordinate mode enables:
        - MySQL agent to return order_ids for user_id=5
        - Postgres agent to use those order_ids to find relevant transactions

    Command:
        python src/main.py chat --work-mode coordinate --show-member-response
    """
    from agents.team import get_data_team
    try:
        get_data_team(
            work_style=work_mode,
            show_member_response=show_member_response,
        ).cli_app()
    except Exception as e:
        typer.echo(f"ERROR: {e}")

def main():
    app()

if __name__ == "__main__":
    main()
