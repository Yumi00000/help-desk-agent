from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

from src.core.settings import AgentSettings
from src.database import BaseDatabaseClient
from src.prompts import read_system_prompt
from src.tools import GetBookingTool, SearchPoliciesTool


class AgentClient:

    def __init__(self, settings: AgentSettings, database: BaseDatabaseClient):
        self.model_name = settings.MODEL
        self.temperature = settings.MODEL_TEMPERATURE
        self.provider = settings.PROVIDER
        self.host = settings.HOST
        self.system_prompt = read_system_prompt()
        self.model = init_chat_model(model_provider=self.provider, model=self.model_name, temperature=self.temperature,
                                     base_url=self.host)
        self.agent = create_agent(
            model=self.model,
            system_prompt=SystemMessage(self.system_prompt),
            tools=[
                SearchPoliciesTool(database=database),
                GetBookingTool(),
            ],
            checkpointer=InMemorySaver()
        )

    def invoke(self, query: str) -> dict[str, Any] | Any:
        return self.agent.invoke({"messages": [{"role": "user", "content": query}]})
