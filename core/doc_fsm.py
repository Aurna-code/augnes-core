import yaml
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from memory.jml import JMLManager
from core.models.judgment import JudgmentMemoryEntry


class DOCFSM:
    def __init__(self, memory, executor, config_path="configs/self_regulate_rules.yaml"):
        self.memory = memory
        self.executor = executor
        self.rules = self._load_regulation_rules(config_path)
        self.jml = JMLManager(path="judgments.jsonl")

    def _load_regulation_rules(self, path):
        if not os.path.exists(path):
            print(f"⚠️  Regulation config not found at: {path}")
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _extract_goal(self, user_input: str) -> dict:
        return {
            "goal_summary": user_input.strip(),
            "original_input": user_input
        }

    def _derive_intent(self, goal: dict) -> dict:
        goal_text = goal.get("goal_summary", "").lower()

        if any(k in goal_text for k in ["code", "function", "import", "rm -rf", "sudo", "os.", "def ", "script"]):
            intent_type = "search_code"
        else:
            intent_type = "general_query"

        strategy_hint = self.jml.recommend_strategy(
            goal_summary=goal["goal_summary"],
            intent_type=intent_type
        )

        intent = {
            "intent_type": intent_type,
            "goal": goal
        }
        if strategy_hint:
            intent["strategy_hint"] = strategy_hint

        return intent

    def _self_regulate(self, goal: dict, intent: dict) -> dict:
        constraints = []
        goal_text = goal.get("goal_summary", "").strip().lower()
        intent_type = intent.get("intent_type", "")

        for rule_name, rule in self.rules.items():
            if intent_type not in rule.get("applicable_intents", []):
                continue

            if rule_name == "empty_goal_blocked" and rule.get("check_empty", False):
                if not goal_text:
                    constraints.append("empty_goal_blocked")

            elif rule_name == "truncate_goal_summary":
                max_len = rule.get("max_length", 100)
                if len(goal_text) > max_len:
                    constraints.append("truncate_goal_summary")

            elif rule_name == "blocked_due_to_security_risk":
                for keyword in rule.get("forbidden_keywords", []):
                    if keyword in goal_text:
                        constraints.append("blocked_due_to_security_risk")
                        break

        return {
            "intent": intent,
            "constraints": constraints,
            "regulated": len(constraints) == 0
        }

    def _store_feedback(self, goal: dict, intent: dict):
        feedback = {
            "goal": goal,
            "intent": intent
        }
        self.memory.store_feedback(feedback)

        entry = JudgmentMemoryEntry(
            task_id=datetime.now(timezone.utc).isoformat(),
            goal_summary=goal["goal_summary"],
            intent_type=intent["intent_type"],
            strategy_hint=intent.get("strategy_hint"),
            regulated=True,  # assumption: always storing post-intent
            constraints=[],
            executor_result=None,
            reward=None,
            feedback_text=None,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        self.jml.save(entry)

    def process(self, user_input: str) -> dict:
        print(f"📥 Input Received: {user_input}")

        goal = self._extract_goal(user_input)
        print(f"[Goal Extracted] {goal}")

        intent = self._derive_intent(goal)
        print(f"[Intent Derived] {intent}")

        regulation = self._self_regulate(goal, intent)

        self._store_feedback(goal, intent)

        if not regulation["regulated"]:
            print(f"❌ Blocked by self_regulate(): {regulation['constraints']}")
            return {
                "error": "Intent blocked due to constraint violation",
                "constraints": regulation["constraints"],
                "goal": goal,
                "intent": intent,
            }

        response = self.executor.act(intent)
        return {
            "goal": goal,
            "intent": intent,
            "regulated": True,
            "response": response,
        }

    def _extract_domain_from_goal(self, goal: dict) -> str:
        return goal.get("domain", "general")

    def _extract_context_features(self, goal: dict) -> Dict[str, float]:
        return {
            "symbolic_depth": 0.0,
            "sequence_length": 0.0
        }
