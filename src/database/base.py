from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document


class BaseDatabaseClient(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]):
        pass

    @abstractmethod
    def search(self, query: str, search_type: str):
        pass
