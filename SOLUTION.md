# Solution — CityWheels help desk agent

## How to install and run

Full details are in [`README.md`](README.md#usage).

```bash
# install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env               # then fill in QDRANT_COLLECTION

# local model and vector store
ollama pull qwen3:4b
ollama pull qwen3-embedding:0.6b
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant

# agent
python main.py --update-db         # load the policy documents into Qdrant (once)
python main.py --start-chat        # chat with the agent

# tests (no Ollama, Qdrant or .env needed)
pytest

# evaluation (needs Ollama, Qdrant and loaded documents)
python -m eval.run_eval            # writes eval/results.md
```

## Model and provider

I chose `qwen3:4b` because it is a nice model for small solutions like this one, and it can also run on low specs.

## How the agent works

The agent uses a vector store database, where the docs (data policies) are placed. Tools: `calculate_refund` to calculate the sum of the possible refund, `search_policies` to read the vector store, and `get_booking` to read the JSON with the booking info.

## Evaluation results

The evaluation passed all questions (11 / 11, see [`eval/results.md`](eval/results.md)). But in my personal test it failed on a follow-up question about a refund: it returned the JSON of the tool call, so I added a middleware to fix that type of errors.

## How I used AI coding assistants

I used AI to write personal notes, to check that the libraries are used according to the library documentation, to help me find bugs sometimes, and to write more tests.

One example where the output was wrong: when it was writing the checkpoint list in my notes, it said that there was an error in `requirements.txt` and that a version must be written another way, or the install will fail. I tested the requirements install and it went fine.

## Limitations

- The model is slow.
- Memory is kept only for the current run; it cannot be used again.
- `calculate_refund` returns "not found" as plain text, not as normal JSON like `get_booking`.

## What I would do next

Next I would improve the middleware: add more checks of the agent's answers and improve error handling.
