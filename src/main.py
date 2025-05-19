
import os
from os.path import join, dirname
from config import Config

dotenv_path = join(dirname(dirname(__file__)), ".env")
os.environ["PROJECT_DIR"] = dirname(dirname(__file__))
Config(env_file=dotenv_path, data_injection={"any": "yes"})

import uuid
import os
import typer
from rich.table import Table
from rich.console import Console
from store import StoreDb
from helper import gen_hash_name

app = typer.Typer()
user_id = "root"

def supported_driver(driver: str) -> bool:
    if driver == "psycopg2":
        return True
    raise False


@app.command()
def add(uri: str, name: str = typer.Option(None)):
    from sqlalchemy import create_engine
    try:
        engine = create_engine(url=uri)
        if supported_driver(driver=engine.driver):
            name = name or gen_hash_name()
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
    from agents.team import data_team
    data_team.cli_app()

def main():
    app()

if __name__ == "__main__":
    main()
