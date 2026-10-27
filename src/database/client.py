from typing import List

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

from src.core.settings import QdrantSettings


class QdrantDatabaseClient:
    def __init__(self, settings: QdrantSettings, embedding: Embeddings):
        self.collection_name = settings.COLLECTION
        self.host = settings.HOST
        self.port = settings.PORT
        self.client = QdrantClient(host=self.host, port=self.port)
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=settings.VECTOR_SIZE, distance=Distance.COSINE)
            )

        self.qdrant = QdrantVectorStore(client=self.client, collection_name=self.collection_name, embedding=embedding)

    def add_documents(self, documents: List[Document]):
        return self.qdrant.add_documents(documents)

    def search(self, query: str, search_type: str):
        return self.qdrant.search(query, search_type)


