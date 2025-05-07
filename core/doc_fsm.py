
import yaml
import os

class DOCFSM:
    def __init__(self, memory, executor, config_path="configs/self_regulate_rules.yaml"):
        self.memory = memory
        self.executor = executor
        self.rules = self._load_regulation_rules(config_path)

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
            return {"intent_type": "search_code", "goal": goal}

        return {"intent_type": "general_query", "goal": goal}

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

    def process(self, user_input: str) -> dict:
        print(f"📥 Input Received: {user_input}")

        goal = self._extract_goal(user_input)
        print(f"[Goal Extracted] {goal}")

        intent = self._derive_intent(goal)
        print(f"[Intent Derived] {intent}")

        regulation = self._self_regulate(goal, intent)

        # 차단 여부와 관계없이 저장
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
