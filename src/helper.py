import uuid
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.models.base import Model
from config import Config

def with_spinner(task_description: str, fn):
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
    return f"db-{uuid.uuid4().hex[:length]}"

def supported_driver(driver: str) -> bool:
    if driver == "psycopg2":
        return True
    if driver =="pymysql":
        return True
    if driver == "native":
        return True
    raise False

def db_name(driver: str) -> str:
    if driver == "psycopg2":
        return "PostgreSQL Database"
    if driver == "pymysql":
        return "MySQL Database"
    if driver == "native":
        return "Clickhouse"
    raise ValueError(f"Unsupported database driver: {driver}")

def agent_name(db_name: str) -> str:
    return f"sql-agent-{db_name}"

def get_model(model_id: str) -> Model:
    model: Model =  None
    provider, model_name = model_id.split(":")
    if provider == "openai":
        if not Config().open_ai_key:
            raise ValueError(f"OPENAI_API_KEY not set. Please set the OPENAI_API_KEY environment variable.")
        model = OpenAIChat(id=model_name)
    elif provider == "google":
        if not Config().google_api_key:
            raise ValueError(f"GOOGLE_API_KEY not set. Please set the GOOGLE_API_KEY environment variable.")
        model = Gemini(id=model_name)
    elif provider == "anthropic":
        if not Config().anthropic_api_key:
            raise ValueError(f"ANTHROPIC_API_KEY not set. Please set the ANTHROPIC_API_KEY environment variable.")
        model = Claude(id=model_name)
    elif provider == "groq":
        if not Config().groq_api_key:
            raise ValueError(f"GROQ_API_KEY not set. Please set the GROQ_API_KEY environment variable.")
        model = Groq(id=model_name)
    else:
        raise ValueError(f"Unsupported model provider: {provider}")
    return model
