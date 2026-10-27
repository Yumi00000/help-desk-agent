from pathlib import Path

from decouple import config
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[2]


class AgentSettings(BaseSettings):
    """Agent settings."""
    PROVIDER: str = config("AGENT_PROVIDER")
    HOST: str = config("AGENT_HOST")
    MODEL: str = config("AGENT_MODEL")
    MODEL_TEMPERATURE: float = config("AGENT_MODEL_TEMPERATURE", default=0.0, cast=float)


class QdrantSettings(BaseSettings):
    """Qdrant settings."""
    HOST: str = config("QDRANT_HOST")
    PORT: int = config("QDRANT_PORT", default=6333, cast=int)
    COLLECTION: str = config("QDRANT_COLLECTION")
    VECTOR_SIZE: int = config("QDRANT_VECTOR_SIZE", default=1024, cast=int)


class EmbeddingSettings(BaseSettings):
    MODEL: str = config("EMBEDDING_MODEL")
    DIMENSION: int = config("EMBEDDING_DIMENSION", default=1024, cast=int)

class ChunkSettings(BaseSettings):
    CHUNK_SIZE: int = config("CHUNK_SIZE", default=1000, cast=int)
    CHUNK_OVERLAP: int = config("CHUNK_OVERLAP", default=0, cast=int)


class DataSettings(BaseSettings):
    """Data settings."""
    DATA_PATH: Path = BASE_DIR / config("DATA_PATH", default="data")
    POLICIES_PATH: Path = DATA_PATH / "policies"
    BOOKINGS_PATH: Path = DATA_PATH / "bookings.json"


class Settings:
    """Settings."""
    agent = AgentSettings()
    qdrant = QdrantSettings()
    embedding = EmbeddingSettings()
    chunk = ChunkSettings()
    data = DataSettings()
    system_prompt_path: str = config("SYSTEM_PROMPT_PATH")


settings = Settings()
