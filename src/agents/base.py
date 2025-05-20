from typing import Optional
from agno.agent import Agent, AgentKnowledge
from agno.tools.reasoning import ReasoningTools
from agno.tools.sql import SQLTools
from agno.tools.file import FileTools
from textwrap import dedent

from agents.promt import (
    additional_context,
    description, 
    get_sql_instruction
)
from constants import (
    IMAGES_PATH,
    MEMBER_MODEL_NAME,
    ANALYZE_MODEL_NAME
)

from sqlalchemy import Engine
from helper import (
    db_name,
    get_model,
)

def get_sql_agent(
    name: str = "SQL Agent",
    model_id: str = MEMBER_MODEL_NAME,
    reasoning: bool = False,
    debug_mode: bool = True,
    db_engine: Optional[Engine] = None,
    knowledge_base: Optional[AgentKnowledge] = None,
    semantic_model: str = "",
) -> Agent:
    """
    Create a SQL Agent capable of querying databases using natural language instructions.

    Parameters:
    - name: Agent identifier and display name.
    - model_id: Language model backend to use (e.g., OpenAI GPT model ID).
    - reasoning: Whether to include reasoning tools for chain-of-thought or justification.
    - debug_mode: Enables detailed logs, tool visibility, and chat history traceability.
    - db_engine: SQLAlchemy engine to access the target database.
    - knowledge_base: Optional vectorized knowledge base (e.g., Chroma, Qdrant).
    - semantic_model: Serialized semantic metadata about the database.

    Returns:
    - An Agent instance equipped with SQLTools, optional reasoning, and knowledge-enhanced instructions.
    """
    # Load the language model specified
    model = get_model(model_id=model_id)

    # Attach core tools: SQL access and file saving
    tools = [
        SQLTools(list_tables=False, db_engine=db_engine),
    ]

    # Optionally add reasoning toolset for higher-level tasks
    if reasoning:
        tools.append(ReasoningTools(add_instructions=True, add_few_shot=True))

    # Build the agent object
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        knowledge=knowledge_base,
        tools=tools,
        description=description,
        # Dynamically inject SQL-specific instructions based on DB type
        instructions=get_sql_instruction(datadabse_model=db_name(driver=db_engine.driver)),
        additional_context=additional_context(semantic_model=semantic_model),
        search_knowledge=True,
        read_chat_history=True,
        read_tool_call_history=True,
        debug_mode=debug_mode,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        show_tool_calls=debug_mode,
        add_name_to_instructions=True,
    )

def get_structure_usage_explainer(
    name: str = "Structure Usage Explainer",
    model_id: str = ANALYZE_MODEL_NAME
) -> Agent:
    """
    Returns an Agent that explains in what scenarios a database structure should be used.
    This agent does not describe specific tables or columns, only the general use of the structure.
    """
    model = get_model(model_id=model_id)
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are Structure Usage Explainer.",
        # Instruction to limit the agent's output to structural usage without column/table details
        instructions=dedent(f"""\
            You are a Database Explainer.

            When the user provides input, follow these steps:

            1. Understand the schema and structure of the database.
            2. Describe the tables and their associated columns.
            3. Explain in what situations this structure would be useful or appropriate.

            <rules>
            - Return a description of the structure, including tables and their columns.
            - Also explain when and why this structure would be useful in practice.
            - Keep output readable and informative for someone unfamiliar with the schema.
            </rules>
        """),
        debug_mode=False,
    )

def get_structure_explainer_with_example(
    name: str = "Structure Usage with Example",
    model_id: str = ANALYZE_MODEL_NAME
) -> Agent:
    """
    Returns an Agent that explains a database structure and when it is useful, along with an example query.
    Includes instruction to describe table usage and generate a sample query for context.
    """
    model = get_model(model_id=model_id)
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are Structure Usage with Example.",
        # Instructions include structured analysis and query example
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
            - Always include at least one example query that demonstrates a typical use case for the identified table(s). The query must be valid and follow correct SQL syntax.
            </rules>
        """),
        debug_mode=False,
    )

def get_table_use_case_extractor(
    name: str = "Table Use Case Extractor",
    model_id: str = ANALYZE_MODEL_NAME
) -> Agent:
    """
    Returns an Agent that extracts table information and use cases in JSON format.
    Designed to output clean structured data with no extra explanation.
    """
    model = get_model(model_id=model_id)
    return Agent(
        name=name,
        model=model,
        agent_id=name,
        description="You are a Table Use Case Extractor.",
        # Output is strictly structured JSON with table name, description, and typical use case
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
