from abc import ABC
from typing import List

from langchain_core.embeddings import Embeddings
from src.core.settings import EmbeddingSettings
from langchain_ollama.embeddings import OllamaEmbeddings


class EmbeddingsClient(Embeddings):
    def __init__(self, settings: EmbeddingSettings):
        self.model = settings.MODEL
        self.dimensions = settings.DIMENSION

        self.embeddings = OllamaEmbeddings(model=self.model, dimensions=self.dimensions)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
