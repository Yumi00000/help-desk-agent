# help-desk-agent

## Code structure

```
.
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
├── .env.exempel                   # Example environment variables (copy to .env)
└── src/
    ├── core/
    │   └── settings.py            # App settings (Agent, Qdrant, Embedding), read from .env
    ├── database/                  # Database / vector store (Qdrant) access
    ├── embeddings/                # Embedding model setup
    ├── llm/                       # LLM (Ollama) client and prompts
    ├── tools/                     # Tools the agent can call
    └── assignments-docs/          # Source data for the agent
        ├── bookings.json          # Sample bike rental bookings
        └── policies/
            ├── cancellations.md   # Cancellation and refund rules
            ├── faq.md             # Frequently asked questions
            └── prices.md          # Rental prices and fees
```

## Environment variables

Settings are read from `.env` with `python-decouple`. Put comments on their own lines in `.env`. A comment after `=` becomes part of the value.

| Variable | Required | Default | Description |
|---|---|---|---|
| `AGENT_HOST` | yes | — | Ollama host, e.g. `http://localhost:11434` |
| `AGENT_MODEL` | yes | — | LLM model name, e.g. `qwen3:4b` |
| `AGENT_MODEL_TEMPERATURE` | no | `0.0` | LLM model temperature |
| `QDRANT_HOST` | yes | — | Qdrant host, e.g. `localhost` |
| `QDRANT_PORT` | no | `6333` | Qdrant REST port |
| `QDRANT_COLLECTION` | yes | — | Qdrant collection name |
| `QDRANT_VECTOR_SIZE` | no | `1024` | Vector size of the Qdrant collection |
| `EMBEDDING_MODEL` | yes | — | Embedding model, e.g. `Qwen/Qwen3-Embedding-0.6B` |
| `EMBEDDING_DIMENSION` | no | `1024` | Vector size, must match the embedding model |

Example `.env`:

```
# Agent Settings
# Ollama host - default http://localhost:11434
AGENT_HOST=http://localhost:11434
# Model name
AGENT_MODEL=qwen3:4b
# Model temperature
AGENT_MODEL_TEMPERATURE=0.0

# Qdrant Settings
# Qdrant host - default localhost
QDRANT_HOST=localhost
# Qdrant port - default 6333
QDRANT_PORT=6333
QDRANT_COLLECTION=
QDRANT_VECTOR_SIZE=1024
# Embedding Settings
# Name of embedding model
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B
#Embedding DIMENSION
EMBEDDING_DIMENSION=1024
```
