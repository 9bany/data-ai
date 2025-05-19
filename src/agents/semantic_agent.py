from agno.agent import Agent
from textwrap import dedent
from helper import get_model

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
    model = get_model(model_id=model_id)
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are Database explainer.",
        instructions=instructions,
        debug_mode=False,
    )
