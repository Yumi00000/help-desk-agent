from langchain_core.documents import Document

from src.database import BaseDatabaseClient
from src.tools import SearchPoliciesTool


class FakeDatabase(BaseDatabaseClient):
    def __init__(self, texts: list[str]):
        self.texts = texts
        self.searches = []

    def add_documents(self, documents):
        pass

    def search(self, query, search_type):
        self.searches.append((query, search_type))
        return [Document(page_content=text) for text in self.texts]


class TestSearchPolicies:
    def test_search_returns_document_text(self):
        database = FakeDatabase(["Cancellation rules", "Prices"])
        result = SearchPoliciesTool(database=database).run("refund")
        assert result == "Cancellation rules\n\nPrices"

    def test_search_sends_query_to_database(self):
        database = FakeDatabase(["Prices"])
        SearchPoliciesTool(database=database).run("e-bike price")
        assert database.searches == [("e-bike price", "similarity")]

    def test_search_without_results(self):
        result = SearchPoliciesTool(database=FakeDatabase([])).run("scooters")
        assert result == ""

    def test_tool_definition(self):
        search_tool = SearchPoliciesTool(database=FakeDatabase([]))
        assert search_tool.name == "search_policies"
        assert list(search_tool.args) == ["query"]
