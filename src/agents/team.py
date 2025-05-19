import typer
from typing import List
from agents.agent import get_sql_agent
from store import StoreDb

from agno.agent import Agent
from agno.knowledge.json import JSONKnowledgeBase
from agno.team.team import Team
from constants import USER_ID
from helper import (
    agent_name as map_agent_name,
    get_model
)

from config import Config

def get_agents() -> List[Agent]:
    list_agents: List[Agent] = []
    databases = StoreDb().app_store.get_all()
    for el in databases:
        from sqlalchemy import create_engine
        try:
            engine = create_engine(url=el.uri)
            agent_name = map_agent_name(el.name)
            vector = StoreDb().knowleged_base_db(collection=agent_name)
            knowledge_base = JSONKnowledgeBase(vector_db=vector)
            agent = get_sql_agent(
                name=agent_name,
                debug_mode=Config().app_config.is_debug(),
                db_engine=engine, 
                knowledge_base=knowledge_base,
                semantic_model=el.meta_data,
            )
            list_agents.append(agent)
        except Exception as e:
            typer.echo(f"Failed to load agent for {el.name}: {e}")
            exit(0)
    return list_agents

agents = get_agents()

analyst_agent = Agent(
    name="Analyst Agent",
    role="Analyzes SQL result data",
    instructions=[
        "Interpret the SQL output and summarize insights, trends, anomalies, and comparisons.",
        "Provide clear, concise analysis with bullet points if needed.",
        "Do not include raw SQL or database code."
    ]
)
agents.append(analyst_agent)

explainer_agent = Agent(
    name="Explanation Agent",
    role="Turns technical output into natural language summary",
    instructions=[
        "Rephrase the analysis into user-friendly language.",
        "Add helpful context if needed, and make the explanation accessible to non-technical users.",
        "Avoid using database jargon—focus on clarity."
    ]
)
agents.append(explainer_agent)

data_team = Team(
    name="Data Team",
    mode="route",
    model=get_model("openai:gpt-4.5-preview"),
    members=agents,
    show_tool_calls=True,
    markdown=True,
    description="A collaborative team that extracts, analyzes, and explains structured data.",
    instructions = [
        "Your goal is to collaboratively analyze a user's data-related question and produce a detailed, accurate, and well-structured response.",
        "First, the SQL Agent will interpret the question, translate it into SQL queries, and execute them to retrieve the relevant data.",
        "Then, the Analyst Agent will analyze the data output, extract insights, and generate summaries with trends, comparisons, or explanations.",
        "Next, the Explanation Agent will rewrite the analysis in natural language for end-user readability, adding context if needed.",
        "Finally, review the full response for clarity, correctness, and completeness before replying to the user.",
        "Ensure that the final response is informative, easy to understand, and backed by accurate data.",
        "If any step fails due to missing data or unsupported queries, provide a polite and helpful fallback message.",
    ],
    knowledge=StoreDb().data_team_knowledge,
    search_knowledge=True,
    show_members_responses=True,
    num_history_runs=50,
    enable_team_history=True,
    user_id=USER_ID
)