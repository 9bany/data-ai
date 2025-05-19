
import os
from os.path import join, dirname
from config import Config

dotenv_path = join(dirname(dirname(__file__)), ".env")
os.environ["PROJECT_DIR"] = dirname(dirname(__file__))
Config(env_file=dotenv_path, data_injection={"any": "yes"})

import os
import typer
from rich.table import Table
from rich.console import Console
from store import StoreDb
from helper import gen_hash_name, with_spinner
from agno.utils.log import logger
from agents.knowledge import process_database

logger.setLevel(Config().app_config.log_level)

app = typer.Typer()
user_id = "root"

def supported_driver(driver: str) -> bool:
    if driver == "psycopg2":
        return True
    if driver =="pymysql":
        return True
    raise False

@app.command()
def add(uri: str, name: str = typer.Option(None)):
    from sqlalchemy import create_engine
    try:
        engine = create_engine(url=uri)
        if supported_driver(driver=engine.driver) == True:
            name = name or gen_hash_name()
            StoreDb().app_store.create({
                "name": name,
                "uri": uri,
                "driver": engine.driver
            })
            load_database = lambda: process_database(name=name, uri=uri)
            with_spinner("Analyze & load database knowledge", load_database)
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
        typer.echo(f"ERROR: {e}")

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
    from agents.team import data_team
    data_team.cli_app()

def main():
    app()

if __name__ == "__main__":
    main()
