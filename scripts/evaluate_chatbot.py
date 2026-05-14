from __future__ import annotations

import argparse
import json
from pathlib import Path

from health_system_chatbot.config import load_config
from health_system_chatbot.evaluation import evaluate_dataset


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="evaluation/ground_truth/stage1_questions_v2.jsonl")
    parser.add_argument("--output", default="evaluation/chatbot/results/iteration_001.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no-llm", action="store_true")
    args = parser.parse_args()

    config = load_config()
    payload = evaluate_dataset(
        dataset=config.project_root / Path(args.dataset),
        output=config.project_root / Path(args.output),
        limit=args.limit,
        allow_llm=not args.no_llm,
        config=config,
    )
    print(json.dumps(payload["summary"], indent=2, ensure_ascii=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

