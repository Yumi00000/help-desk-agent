import json

from langchain_core.documents import Document
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

from src.core.settings import AgentSettings
from src.database import BaseDatabaseClient
from src.llm import AgentClient


class FakeModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


class FakeDatabase(BaseDatabaseClient):
    def add_documents(self, documents):
        pass

    def search(self, query, search_type):
        return [Document(page_content="E-bike: 40 EUR per day.")]


def make_agent(monkeypatch, *answers: AIMessage) -> AgentClient:
    model = FakeModel(messages=iter(answers))
    monkeypatch.setattr("src.llm.client.init_chat_model", lambda **kwargs: model)
    return AgentClient(AgentSettings(), FakeDatabase())


def tool_call(name: str, **args) -> AIMessage:
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": f"call_{name}"}])


class TestAgent:
    def test_agent_calls_tool_and_answers(self, monkeypatch):
        agent = make_agent(monkeypatch, tool_call("get_booking", booking_id="CW-1005"), AIMessage(content="It is cancelled."))
        messages = agent.invoke("What is the status of CW-1005?", thread_id="test")["messages"]
        tool_result = json.loads(messages[-2].content)
        assert tool_result["status"] == "cancelled"
        assert messages[-1].content == "It is cancelled."

    def test_refund_is_calculated_by_tool(self, monkeypatch):
        agent = make_agent(monkeypatch, tool_call("calculate_refund", booking_id="CW-1002"), AIMessage(content="You get 340 EUR."))
        messages = agent.invoke("How much do I get back for CW-1002?", thread_id="test")["messages"]
        assert json.loads(messages[-2].content)["total_refund_eur"] == 340.0

    def test_agent_answers_without_tool(self, monkeypatch):
        agent = make_agent(monkeypatch, AIMessage(content="Please contact the staff."))
        messages = agent.invoke("What is the capital of France?", thread_id="test")["messages"]
        assert [message.type for message in messages] == ["human", "ai"]

    def test_text_tool_call_is_executed_and_hidden(self, monkeypatch):
        text_call = json.dumps({"name": "search_policies", "arguments": {"query": "e-bike price"}})
        agent = make_agent(monkeypatch, AIMessage(content=text_call), AIMessage(content="40 EUR per day."))
        answer = "".join(agent.stream("How much is an e-bike?", thread_id="test"))
        assert answer == "40 EUR per day."
