from pathlib import Path

from src.chunker import ChunkerClient
from src.core.settings import ChunkSettings, EmbeddingSettings, QdrantSettings
from src.database import BaseDatabaseClient, QdrantDatabaseClient
from src.embeddings import EmbeddingsClient


def add_docs_to_db(path: Path, database: BaseDatabaseClient, chunker: ChunkerClient):
    documents = chunker.chunk_file(path)
    database.add_documents(documents)
    print(f"{path.name}: {len(documents)} chunks")


if __name__ == "__main__":
    chunker = ChunkerClient(ChunkSettings())
    embedding_client = EmbeddingsClient(EmbeddingSettings())
    database = QdrantDatabaseClient(QdrantSettings(), embedding_client)

    print(Path(__file__).resolve().parents[1] / "data" / "policies" )
    policy_path = Path(__file__).resolve().parents[1] / "data" / "policies"
    for policy_file in policy_path.iterdir():
        add_docs_to_db(policy_file, database, chunker)

