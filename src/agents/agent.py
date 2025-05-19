from typing import Optional
from agno.agent import Agent, AgentKnowledge
from agno.tools.reasoning import ReasoningTools
from agno.tools.sql import SQLTools
from agno.tools.file import FileTools
from .promt import (
    additional_context,
    description, 
    get_sql_instruction
)
from constants import IMAGES_PATH
from sqlalchemy import Engine
from helper import (
    db_name,
    get_model,
)

def get_sql_agent(
    name: str = "SQL Agent",
    model_id: str = "openai:gpt-4o",
    reasoning: bool = False,
    debug_mode: bool = True,
    db_engine: Optional[Engine] = None,
    knowledge_base: Optional[AgentKnowledge] = None,
) -> Agent:
    model = get_model(model_id=model_id)
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
        instructions=get_sql_instruction(datadabse_model=db_name(engine=db_engine.driver)),
        additional_context=additional_context,
        search_knowledge=True,
        read_chat_history=True,
        read_tool_call_history=True,
        debug_mode=debug_mode,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
    )