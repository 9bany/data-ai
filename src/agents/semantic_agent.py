from agno.agent import Agent
from textwrap import dedent
from helper import get_model

def get_structure_usage_explainer(
    name: str = "Structure Usage Explainer",
    model_id: str = "openai:gpt-4o"
) -> Agent:
    model = get_model(model_id=model_id)
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are Structure Usage Explainer.",
        instructions=dedent(f"""\
            You are a Database Explainer.

            When the user provides input, follow these steps:

            1. Understand the structure or schema mentioned.
            2. Do not describe tables or columns.
            3. Only explain in what situations this database structure would be useful or appropriate.

            <rules>
            - Only return an explanation of when and why this database structure should be used. Do not return table or column details.
            </rules>
        """),
        debug_mode=False,
    )

def get_structure_explainer_with_example(
    name: str = "Structure Usage with Example",
    model_id: str = "openai:gpt-4o"
) -> Agent:
    model = get_model(model_id=model_id)
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are Structure Usage with Example.",
        instructions=dedent(f"""\
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
            - Always include at least one example query that demonstrates a typical use case for the identified table(s).
            </rules>
        """),
        debug_mode=False,
    )

def get_table_use_case_extractor(
    name: str = "Table Use Case Extractor",
    model_id: str = "openai:gpt-4o"
) -> Agent:
    model = get_model(model_id=model_id)
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are a Table Use Case Extractor.",
        instructions=dedent(f"""\
            You are an agent that reviews database schemas and summarizes key information about tables.

            When the user provides input, follow these steps:

            1. Identify all the tables available in the database.
            2. For each table, summarize what it contains and what it's for.
            3. Describe a typical use case for querying each table.

            <rules>
            - Only return a structured JSON object containing a list of tables.
            - Each item must contain: `table_name`, `table_description`, and `Use Case`.
            - Do not include SQL queries or table relationships.
            - Output only valid JSON. Do not add explanation outside the JSON.
            </rules>
        """),
        debug_mode=False,
    )
