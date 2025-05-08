# memory/jml.py

import json
import uuid
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# 🔵 v0 구조: 전략 실험 중심
@dataclass
class StrategyResult:
    name: str
    success_rate: float
    reward_avg: float
    convergence_score: Optional[float] = None
    notes: Optional[str] = None

@dataclass
class JudgmentMemoryEntry_v0:
    domain: str
    task_id: str
    strategies_tested: List[StrategyResult]
    final_decision: str
    confidence: float
    context_features: Dict[str, float]
    timestamp: str
    meta_comment: Optional[str] = None
    id: str = uuid.uuid4().hex

# 🔴 v1 구조: 실행 기반 판단 기록 (pydantic)
try:
    from core.models.judgment import JudgmentMemoryEntry as JudgmentMemoryEntry_v1
except ImportError:
    JudgmentMemoryEntry_v1 = None  # 경량 테스트용 방어 코드

class JMLManager:
    def __init__(self, path="judgments.jsonl"):
        self.path = path
        if not os.path.exists(self.path):
            open(self.path, 'w').close()

    def save(self, entry):
        """두 버전 모두 지원"""
        with open(self.path, 'a') as f:
            if isinstance(entry, JudgmentMemoryEntry_v0):
                f.write(json.dumps(asdict(entry)) + "\n")
            elif JudgmentMemoryEntry_v1 and isinstance(entry, JudgmentMemoryEntry_v1):
                f.write(entry.model_dump_json() + "\n")
            else:
                raise ValueError("Unsupported entry format")

    def load_all_entries(self) -> Tuple[List[JudgmentMemoryEntry_v0], List[JudgmentMemoryEntry_v1]]:
        v0_entries = []
        v1_entries = []
        with open(self.path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                try:
                    if "strategies_tested" in data:
                        data["strategies_tested"] = [StrategyResult(**s) for s in data["strategies_tested"]]
                        v0_entries.append(JudgmentMemoryEntry_v0(**data))
                    elif "goal_summary" in data and JudgmentMemoryEntry_v1:
                        v1_entries.append(JudgmentMemoryEntry_v1(**data))
                except Exception as e:
                    print("⚠️ Invalid entry skipped:", e)
        return v0_entries, v1_entries

    def recommend_strategy(
        self,
        goal_summary: Optional[str] = None,
        intent_type: Optional[str] = None,
        domain: Optional[str] = None,
        context_feature: Optional[Dict[str, float]] = None
    ) -> Optional[str]:
        v0_entries, v1_entries = self.load_all_entries()

        # 1️⃣ v1 기반 추천: goal + intent 완전 일치
        if goal_summary and intent_type:
            for e in reversed(v1_entries):
                if e.goal_summary == goal_summary and e.intent_type == intent_type:
                    return e.strategy_hint

        # 2️⃣ v0 기반 fallback: domain 기반 최고 confidence
        if domain and context_feature:
            candidates = [e for e in v0_entries if e.domain == domain]
            if candidates:
                best = max(candidates, key=lambda e: e.confidence)
                return best.final_decision

        return None
