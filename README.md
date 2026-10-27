# help-desk-agent

## Code structure

```
.
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
├── .env.exempel                   # Example environment variables (copy to .env)
└── src/
    ├── core/
    │   └── settings.py            # App settings (Agent, Qdrant, Embedding, Chunk), read from .env
    ├── chunker/
    │   └── client.py              # Splits Markdown into chunks by headers
    ├── database/
    │   ├── base.py                # Base database client
    │   └── client.py              # Qdrant vector store client
    ├── embeddings/
    │   └── client.py              # Embedding model (Ollama)
    ├── llm/
    │   └── client.py              # Agent (Ollama LLM + tools)
    ├── prompts/
    │   ├── reader.py              # Reads the system prompt
    │   └── SYSTEM_PROMPT.md       # System prompt for the agent
    ├── scripts/
    │   └── add_docs_to_db.py      # Adds documents to Qdrant
    ├── tools/
    │   └── search.py              # search_documents tool
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
| `AGENT_PROVIDER` | yes | — | LLM provider, e.g. `ollama` |
| `AGENT_HOST` | yes | — | Ollama host, e.g. `http://localhost:11434` |
| `AGENT_MODEL` | yes | — | LLM model name, e.g. `qwen3:4b` |
| `AGENT_MODEL_TEMPERATURE` | no | `0.0` | LLM model temperature |
| `QDRANT_HOST` | yes | — | Qdrant host, e.g. `localhost` |
| `QDRANT_PORT` | no | `6333` | Qdrant REST port |
| `QDRANT_COLLECTION` | yes | — | Qdrant collection name |
| `QDRANT_VECTOR_SIZE` | no | `1024` | Vector size of the Qdrant collection |
| `EMBEDDING_MODEL` | yes | — | Embedding model, e.g. `qwen3-embedding:0.6b` |
| `EMBEDDING_DIMENSION` | no | `1024` | Vector size, must match the embedding model |
| `SYSTEM_PROMPT_PATH` | yes | — | Folder with `SYSTEM_PROMPT.md`, relative to the project root, e.g. `src/prompts` |
| `CHUNK_SIZE` | no | `1000` | Max chunk size in characters |
| `CHUNK_OVERLAP` | no | `0` | Overlap between chunks in characters |

Example `.env`:

```
# Agent Settings
# LLM provider - default ollama
AGENT_PROVIDER=ollama
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
EMBEDDING_MODEL=qwen3-embedding:0.6b
#Embedding DIMENSION
EMBEDDING_DIMENSION=1024

# Prompts
# Folder with SYSTEM_PROMPT.md, relative to the project root
SYSTEM_PROMPT_PATH=src/prompts

# Chunk Settings
# Max chunk size in characters
CHUNK_SIZE=1000
CHUNK_OVERLAP=0
```
