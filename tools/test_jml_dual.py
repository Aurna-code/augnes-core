
import sys, os
sys.path.append(os.path.abspath("."))

from core.models.judgment import JudgmentMemoryEntry
from memory.jml import JMLManager
from datetime import datetime, timezone

jml = JMLManager()

# 1. 테스트용 v1 판단 저장
entry = JudgmentMemoryEntry(
    task_id=datetime.now(timezone.utc).isoformat(),
    goal_summary="How do I list files in Python?",
    intent_type="general_query",
    strategy_hint="use pathlib + glob",
    regulated=False,
    constraints=[],
    executor_result="execution not needed",
    reward=0.7,
    feedback_text="clean general query",
    timestamp=datetime.now(timezone.utc).isoformat()
)

jml.save(entry)

# 2. 전략 추천 테스트
recommended = jml.recommend_strategy(
    goal_summary="How do I list files in Python?",
    intent_type="general_query"
)

print(f"📌 전략 추천 (v1 기반): {recommended}")





'''


# v0 테스트
domain = "math_induction"
features = {"symbolic_depth": 0.8}

fallback = jml.recommend_strategy(domain=domain, context_feature=features)
print(f"📎 Fallback 추천 (v0 기반): {fallback}")
'''