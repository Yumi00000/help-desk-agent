from decouple import config
from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    """Agent settings."""
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


class Settings:
    """Settings."""
    agent = AgentSettings()
    qdrant = QdrantSettings()
    embedding = EmbeddingSettings()

settings = Settings()
