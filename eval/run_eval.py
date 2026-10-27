import json
import uuid
from pathlib import Path

from src.core.settings import AgentSettings, EmbeddingSettings, QdrantSettings
from src.database import QdrantDatabaseClient
from src.embeddings import EmbeddingsClient
from src.llm import AgentClient

EVAL_DIR = Path(__file__).resolve().parent


def main():
    questions = json.loads((EVAL_DIR / "questions.json").read_text())
    database = QdrantDatabaseClient(QdrantSettings(), EmbeddingsClient(EmbeddingSettings()))
    agent = AgentClient(AgentSettings(), database)

    lines = ["| Question | Tool | Expected | Result | Answer |", "|---|---|---|---|---|"]
    passed = 0
    for case in questions:
        messages = agent.invoke(case["question"], thread_id=str(uuid.uuid4()))["messages"]
        answer = messages[-1].content.strip()
        tools_called = [call["name"] for message in messages for call in getattr(message, "tool_calls", [])]

        ok = case["expected"].lower() in answer.lower() and (case["tool"] is None or case["tool"] in tools_called)
        passed += ok
        print("PASS" if ok else "FAIL", case["question"])

        answer = answer.replace("\n", " ").replace("|", "/")[:150]
        lines.append(f"| {case['question']} | {case['tool'] or '—'} | {case['expected']} | {'PASS' if ok else 'FAIL'} | {answer} |")

    summary = f"**{passed} / {len(questions)} passed**"
    (EVAL_DIR / "results.md").write_text(f"# Evaluation results\n\n{summary}\n\n" + "\n".join(lines) + "\n")
    print(summary)


if __name__ == "__main__":
    main()
