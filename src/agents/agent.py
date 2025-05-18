from typing import Optional
from agno.agent import Agent, AgentKnowledge
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.sql import SQLTools
from agno.tools.file import FileTools
from .promt import (
    additional_context,
    description, 
    instructions
)
from constants import IMAGES_PATH
from sqlalchemy import Engine

def get_sql_agent(
    name: str = "SQL Agent",
    model_id: str = "openai:gpt-4o",
    reasoning: bool = False,
    debug_mode: bool = True,
    db_engine: Optional[Engine] = None,
    knowledge_base: Optional[AgentKnowledge] = None,
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

    tools = [
        SQLTools(list_tables=False, db_engine=db_engine),
        FileTools(base_dir=IMAGES_PATH),
    ]
    if reasoning:
        tools.append(ReasoningTools(add_instructions=True, add_few_shot=True))

    return Agent(
        name=name,
        model=model,
        agent_id=name,
        knowledge=knowledge_base,
        tools=tools,
        description=description,
        instructions=instructions,
        additional_context=additional_context,
        search_knowledge=True,
        read_chat_history=True,
        read_tool_call_history=True,
        debug_mode=debug_mode,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
    )