# help-desk-agent

## Usage

Before running:

- Ollama running with the models from `.env`: `ollama pull qwen3:4b` and `ollama pull qwen3-embedding:0.6b`
- Qdrant running: `docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant`
- `.env` created from `.env.example`

```bash
python main.py                           # show help
python main.py --update-db               # rebuild the Qdrant collection from data/policies
python main.py --start-chat              # chat with the agent
python main.py --update-db --start-chat  # rebuild the collection, then chat
```

| Option | What it does |
|---|---|
| `--update-db` | Deletes the Qdrant collection and loads all files from `data/policies/` again (chunk → embed → store) |
| `--start-chat` | Starts a chat. Answers are streamed token by token. The agent remembers earlier questions in the same chat |

In the chat, type `/exit` or press Ctrl+C / Ctrl+D to quit. Run `--update-db` once before the first chat, and again after changing the policy files.

## Code structure

```
.
├── main.py                        # CLI: chat with the agent (streaming), rebuild the Qdrant collection
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment variables (copy to .env)
├── data/                          # Source data for the agent
│   ├── bookings.json              # Sample bike rental bookings
│   └── policies/
│       ├── cancellations.md       # Cancellation and refund rules
│       ├── faq.md                 # Frequently asked questions
│       └── prices.md              # Rental prices and fees
└── src/
    ├── core/
    │   └── settings.py            # App settings (Agent, Qdrant, Embedding, Chunk, Data), read from .env
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
    ├── services/
    │   ├── calculations/
    │   │   └── calculate_refunds.py # CalculateRefunds: refund formula from the cancellation rules
    │   └── data_management/
    │       └── load_booking.py    # BookingLoader: reads bookings.json, finds a booking by id
    └── tools/
        ├── search.py              # search_policies tool
        ├── get_booking.py         # get_booking tool
        └── calculate_refund.py    # calculate_refund tool
```

## Agent tools

| Tool | Input | What it returns |
|---|---|---|
| `search_policies` | `query` | The most relevant parts of the policy documents (from Qdrant) |
| `get_booking` | `booking_id`, e.g. `CW-1001` | The details of one booking, or `Booking ... not found.` |
| `calculate_refund` | `booking_id`, e.g. `CW-1001` | Refund if the booking is cancelled now: hours before start, refund %, rental / deposit / booking fee refund and total in EUR, or `Booking ... not found.` |

### Refund rules (`calculate_refund`)

The amount is calculated by code, not by the model, with the fixed current date **2026-06-10 09:00 +02:00**.

| Booking | Refund |
|---|---|
| Status `in_progress`, `completed` or `cancelled` | Nothing |
| `confirmed`, 48 hours or more before the start | 100% of the rental price |
| `confirmed`, 24 to 48 hours before the start | 50% of the rental price |
| `confirmed`, less than 24 hours before the start | 0% of the rental price |

The booking fee is never refunded. The deposit is refunded in full when a `confirmed` booking is cancelled.

## Data

CityWheels is a made-up bike rental shop. These files hold the data for its help desk agent.

| File | What it holds |
| --- | --- |
| `data/policies/prices.md` | Bike types, rental prices, add-ons, deposits and late return fees. |
| `data/policies/cancellations.md` | Rules for cancelling or changing a booking, and for refunds. |
| `data/policies/faq.md` | Answers to common questions: opening hours, age limits, payment, what to do when something goes wrong. |
| `data/bookings.json` | Example bookings. |

### Bookings

Each booking in `bookings.json` has these fields:

| Field | Meaning |
| --- | --- |
| `id` | Booking number, for example `CW-1001`. |
| `status` | `confirmed`, `in_progress`, `completed` or `cancelled`. |
| `bike_type` | `city`, `e-bike` or `kids`. |
| `bikes` | How many bikes are booked. |
| `start`, `end` | When the rental starts and ends, with the time zone. |
| `add_ons` | Extras, such as `child_seat`. |
| `rental_price_eur` | Price of the rental itself, with add-ons. |
| `booking_fee_eur` | Fee for booking online. |
| `deposit_eur` | Deposit paid with the booking. |
| `paid_with` | `card` or `voucher`. |

### The current date

The bookings are set in June 2026. So that answers are the same every time, treat the current date and time as:

**2026-06-10 09:00, Europe/Warsaw time (UTC+02:00).**

### Example questions

- What time do you open on Saturday?
- How much is an e-bike for a whole day?
- I want to cancel booking CW-1002. How much will I get back?
- Can my 14-year-old rent an e-bike?
- What is the capital of Australia?

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
| `DATA_PATH` | no | `data` | Folder with `policies/` and `bookings.json`, relative to the project root |
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

# Data
# Folder with policies/ and bookings.json, relative to the project root
DATA_PATH=data

# Chunk Settings
# Max chunk size in characters
CHUNK_SIZE=1000
CHUNK_OVERLAP=0
```
