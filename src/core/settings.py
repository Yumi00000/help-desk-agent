from decouple import config


class AgentSettings:
    """Agent settings."""
    HOST: str = config("AGENT_HOST")
    MODEL: str = config("AGENT_MODEL")
    MODEL_TEMPERATURE: float = config("AGENT_MODEL_TEMPERATURE", default=0.0, cast=float)


class QdrantSettings:
    """Qdrant settings."""
    HOST: str = config("QDRANT_HOST")
    PORT: int = config("QDRANT_PORT", default=6333, cast=int)
    COLLECTION: str = config("QDRANT_COLLECTION")

class EmbeddingSettings:
    MODEL: str = config("EMBEDDING_MODEL")
    DIMENSION: int = config("EMBEDDING_DIMENSION", default=1024, cast=int)


class Settings:
    """Settings."""
    agent = AgentSettings()
    qdrant = QdrantSettings()
    embedding = EmbeddingSettings()

settings = Settings()
