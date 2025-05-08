# tools/convert_feedback.py

import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(".")  # VSCode WSL 또는 CLI 실행을 위한 경로 보정
from core.models.judgment import JudgmentMemoryEntry

INPUT = Path("data/feedback_log.jsonl")
OUTPUT = Path("judgments.jsonl")

with INPUT.open("r", encoding="utf-8") as fin, OUTPUT.open("a", encoding="utf-8") as fout:
    for line in fin:
        raw = json.loads(line.strip())
        try:
            entry = JudgmentMemoryEntry(
                task_id=datetime.utcnow().isoformat(),
                goal_summary=raw["goal"]["goal_summary"],
                intent_type=raw["intent"]["intent_type"],
                strategy_hint=None,
                regulated=False,
                constraints=[],
                executor_result=None,
                reward=None,
                feedback_text=None
            )
            fout.write(entry.json() + "\n")
        except Exception as e:
            print("⛔ Skipped invalid entry:", e)
