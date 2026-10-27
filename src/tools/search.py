from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from src.database import BaseDatabaseClient


class SearchPoliciesInput(BaseModel):
    query: str = Field(description="What to search for in the documents")


class SearchPoliciesTool(BaseTool):
    name: str = "search_policies"
    description: str = "Search documents in the knowledge base and return the most relevant text."
    args_schema: type[BaseModel] = SearchPoliciesInput
    database: BaseDatabaseClient

    def _run(self, query: str) -> str:
        documents = self.database.search(query, "similarity")
        return "\n\n".join(document.page_content for document in documents)
