import argparse
import uuid

from src.chunker import ChunkerClient
from src.core.settings import QdrantSettings, EmbeddingSettings, ChunkSettings, DataSettings, AgentSettings
from src.database import QdrantDatabaseClient
from src.embeddings import EmbeddingsClient
from src.llm import AgentClient
from src.scripts.add_docs_to_db import add_docs_to_db


def ask(agent: AgentClient, user_msg: str, thread_id: str) -> None:
    print("Agent: ", end="", flush=True)
    for token in agent.stream(user_msg, thread_id=thread_id):
        print(token, end="", flush=True)
    print()


def chat(agent: AgentClient, thread_id: str) -> None:
    print("Chat started")
    while True:
        try:
            user_msg = input("\nUser: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if user_msg.lower() == "/exit":
            break
        if user_msg:
            ask(agent, user_msg, thread_id)
    print("Chat ended")


def update_db(embeddings: EmbeddingsClient, database: QdrantDatabaseClient) -> QdrantDatabaseClient:
    database.client.delete_collection(database.collection_name)
    database = QdrantDatabaseClient(QdrantSettings(), embeddings)
    chunker = ChunkerClient(ChunkSettings())
    for policy_file in DataSettings().POLICIES_PATH.iterdir():
        add_docs_to_db(policy_file, database, chunker)
    return database


def main():
    parser = argparse.ArgumentParser(description="CityWheels help desk agent")
    parser.add_argument("--update-db", action="store_true", help="Rebuild the Qdrant collection from data/policies")
    parser.add_argument("--start-chat", action="store_true", help="Start chat")
    args = parser.parse_args()

    if not (args.update_db or args.start_chat):
        parser.print_help()
        return

    embeddings = EmbeddingsClient(EmbeddingSettings())
    database = QdrantDatabaseClient(QdrantSettings(), embeddings)

    if args.update_db:
        database = update_db(embeddings, database)

    if args.start_chat:
        agent = AgentClient(AgentSettings(), database)
        thread_id = str(uuid.uuid4())
        chat(agent=agent, thread_id=thread_id)


if __name__ == "__main__":
    main()
