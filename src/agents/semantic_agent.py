from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
import json
from textwrap import dedent
from constants import IMAGES_PATH
from sqlalchemy import Engine

instructions = dedent(f"""\
    You are a Database Explainer.

    When the user provides input, follow these steps:

    1. Identify the tables being referenced in the user message.
    2. For each table, extract relevant column information.
    3. If specific table rules are provided, you must follow them precisely.
    4. Based on the information gathered, synthesize a unified explanation of the database structure and behavior.
    5. Explain when and why the given database structure would be used.

    <rules>
    - Always return a clear, well-structured explanation of the database.
    - Ensure queries are written to handle duplicate records appropriately.
    - Ensure queries account for null values and edge cases.
    - Return only plain text — do not use Markdown or other formatting.
    - Always explain what type of questions or use cases this database is best suited to answer.
    </rules>
""")

def get_db_explainer(
    name: str = "Database explainer",
    model_id: str = "openai:gpt-4o"
) -> Agent:
    provider, model_name = model_id.split(":")
    if provider == "openai":
        model = OpenAIChat(id=model_name)
    elif provider == "google":
        model = Gemini(id=model_name)
    elif provider == "anthropic":
        model = Claude(id=model_name)
    elif provider == "groq":
        model = Groq(id=model_name)
    else:
        raise ValueError(f"Unsupported model provider: {provider}")
    
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are Database explainer.",
        instructions=instructions,
        debug_mode=False,
    )
