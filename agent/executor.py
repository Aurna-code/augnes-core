# agent/executor.py

class Executor:
    def __init__(self, memory=None):
        """
        행동 실행자 - 외부 명령 처리, API 호출, 검색 등
        - memory: context 기반 행동 보완 (선택)
        """
        self.memory = memory

    def act(self, action_dict: dict) -> str:
        """
        DOCFSM에서 전달받은 결과에 따라 행동 결정 및 수행
        """
        action_type = action_dict.get("final_action")
        payload = action_dict.get("payload")

        if action_type == "search_code":
            return self._simulate_code_search(payload)
        elif action_type == "general_query":
            return self._simulate_general_response(payload)
        else:
            return f"[Executor] Unknown action type: {action_type}"

    def _simulate_code_search(self, payload: dict) -> str:
        query = payload.get("goal_summary", "")
        return f"[Simulated Code Search] 🔍 Searching GitHub for: `{query}`"

    def _simulate_general_response(self, payload: dict) -> str:
        text = payload.get("goal_summary", "")
        return f"[Simulated Response] 🤖 You said: `{text}`"
