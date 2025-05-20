"""
This module contains utility functions for use across the Data-AI platform,
including driver support validation, agent/model selection, naming utilities,
and progress spinners for UI feedback.
"""

import uuid
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.models.base import Model
from config import Config

def with_spinner(task_description: str, fn):
    """
    Display a loading spinner while executing a function.

    Args:
        task_description (str): Message shown while the task is running.
        fn (callable): Function to execute.

    Returns:
        The result of calling `fn`.
    """
    from rich.progress import Progress, SpinnerColumn, TextColumn
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(task_description, total=None)
        result = fn()
        progress.remove_task(task)
        return result

def gen_hash_name(length: int = 6): 
    """
    Generate a unique hash name for identifying a database (or agent).

    Args:
        length (int): Number of characters from the UUID hex.

    Returns:
        str: A formatted hash name, e.g., 'db-a1b2c3'
    """
    return f"db-{uuid.uuid4().hex[:length]}"

def supported_driver(driver: str) -> bool:
    """
    Check if a given database driver is supported.

    Args:
        driver (str): The driver string.

    Returns:
        bool: True if supported, otherwise raises.
    """
    if driver == "psycopg2":
        return True
    if driver == "pymysql":
        return True
    if driver == "native":
        return True
    raise False

def db_name(driver: str) -> str:
    """
    Map driver to a human-readable database name.

    Args:
        driver (str): The driver identifier.

    Returns:
        str: Display name of the database.
    """
    if driver == "psycopg2":
        return "PostgreSQL Database"
    if driver == "pymysql":
        return "MySQL Database"
    if driver == "native":
        return "Clickhouse"
    raise ValueError(f"Unsupported database driver: {driver}")

def agent_name(db_name: str) -> str:
    """
    Generate a standard agent name for a given database.

    Args:
        db_name (str): The logical database name.

    Returns:
        str: Agent name like 'sql-agent-<db>'
    """
    return f"sql-agent-{db_name}"

def get_model(model_id: str) -> Model:
    """
    Create and return a model instance based on model ID.

    Format of model_id: 'provider:model_name'

    Supported providers: openai, google, anthropic, groq

    Args:
        model_id (str): Provider and model name separated by colon.

    Returns:
        Model: An instance of a Model subclass.

    Raises:
        ValueError: If provider is not supported or API key not set.
    """
    model: Model = None
    provider, model_name = model_id.split(":")
    if provider == "openai":
        if not Config().open_ai_key:
            raise ValueError("OPENAI_API_KEY not set. Please set the OPENAI_API_KEY environment variable.")
        model = OpenAIChat(id=model_name)
    elif provider == "google":
        if not Config().google_api_key:
            raise ValueError("GOOGLE_API_KEY not set. Please set the GOOGLE_API_KEY environment variable.")
        model = Gemini(id=model_name)
    elif provider == "anthropic":
        if not Config().anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set. Please set the ANTHROPIC_API_KEY environment variable.")
        model = Claude(id=model_name)
    elif provider == "groq":
        if not Config().groq_api_key:
            raise ValueError("GROQ_API_KEY not set. Please set the GROQ_API_KEY environment variable.")
        model = Groq(id=model_name)
    else:
        raise ValueError(f"Unsupported model provider: {provider}")
    return model
