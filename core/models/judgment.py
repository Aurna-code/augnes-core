# datamodels/judgment.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class JudgmentMemoryEntry(BaseModel):
    task_id: str = Field(..., description="고유 판단 식별자 (예: timestamp 기반)")
    goal_summary: str
    intent_type: str
    strategy_hint: Optional[str] = None
    regulated: bool
    constraints: Optional[List[str]] = []
    executor_result: Optional[str] = None
    reward: Optional[float] = None
    feedback_text: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
