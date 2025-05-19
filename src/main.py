
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

app = typer.Typer()
user_id = "root"

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
def test():
    from agents.semantic_agent import (
        get_structure_usage_explainer,
        get_structure_explainer_with_example,
        get_table_use_case_extractor,
    )
    from sqlalchemy import create_engine
    from agents.knowledge import db_knowledge
    import json
    engine = create_engine(url="mysql+pymysql://root:root@localhost/mysql-data-ai-test")
    db = db_knowledge(engine=engine)
    response = get_table_use_case_extractor().run(json.dumps(db.to_json()))
    print(response.content)

@app.command()
def chat():
    from agents.team import data_team
    try:
        data_team.cli_app()
    except Exception as e:
        typer.echo(f"ERROR: {e}")

def main():
    app()

if __name__ == "__main__":
    main()
