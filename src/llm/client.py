from typing import Any, Iterator, Generator

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessageChunk, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

from src.core.settings import AgentSettings
from src.database import BaseDatabaseClient
from src.llm.middleware import fix_text_tool_calls, parse_text_tool_call
from src.prompts import read_system_prompt
from src.tools import CalculateRefundTool, GetBookingTool, SearchPoliciesTool


class AgentClient:

    def __init__(self, settings: AgentSettings, database: BaseDatabaseClient):
        self.model_name = settings.MODEL
        self.temperature = settings.MODEL_TEMPERATURE
        self.provider = settings.PROVIDER
        self.host = settings.HOST
        self.system_prompt = read_system_prompt()
        self.model = init_chat_model(model_provider=self.provider, model=self.model_name, temperature=self.temperature,
                                     base_url=self.host)
        self.tools = [
            SearchPoliciesTool(database=database),
            GetBookingTool(),
            CalculateRefundTool(),
        ]
        self.tool_names = {tool.name for tool in self.tools}
        self.agent = create_agent(
            model=self.model,
            system_prompt=SystemMessage(self.system_prompt),
            tools=self.tools,
            middleware=[fix_text_tool_calls],
            checkpointer=InMemorySaver()
        )

    def invoke(self, query: str, thread_id: str = "cli") -> dict[str, Any] | Any:
        return self.agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config=RunnableConfig(configurable={"thread_id": thread_id}),
        )

    def stream(self, query: str, thread_id: str = "cli") -> Generator[str | list[str | dict[Any, Any]], Any, None]:
        message_id, pending, is_json = None, "", None
        for chunk, metadata in self.agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            config=RunnableConfig(configurable={"thread_id": thread_id}),
            stream_mode="messages",
        ):
            if not (isinstance(chunk, AIMessageChunk) and isinstance(chunk.content, str) and chunk.content):
                continue
            if chunk.id != message_id:
                if is_json and not parse_text_tool_call(pending, self.tool_names):
                    yield pending
                message_id, pending, is_json = chunk.id, "", None
            if is_json is False:
                yield chunk.content
                continue
            # Hold back text that starts with "{" until the message ends: it may be a tool call written as text
            pending += chunk.content
            if is_json is None and pending.strip():
                is_json = pending.lstrip().startswith("{")
                if not is_json:
                    yield pending
        if is_json and not parse_text_tool_call(pending, self.tool_names):
            yield pending
