class StrategicReasoner:
    def __init__(self, config=None):
        """
        전략적 판단을 담당하는 Reasoner
        - 입력 문장을 받아 Goal 설정 전의 판단을 수행함
        - config: 판단 기준/룰 등을 설정할 수 있는 dict
        """
        self.config = config or {}

    def analyze(self, user_input: str) -> dict:
        """
        입력 문장을 분석하여 goal 생성을 위한 판단 정보를 반환
        예시 반환:
        {
            "type": "general_query",   # or "contradiction", "emotion_trigger", ...
            "notes": "Simple informational query"
        }
        """
        # TODO: 고도화된 판단 로직 (감정, 베이즈, RL 등) 이후 확장 예정

        lowered = user_input.lower()
        if any(keyword in lowered for keyword in ["not", "but", "however"]):
            return {"type": "contradiction", "notes": "Detected contrastive logic."}
        elif "feel" in lowered or "i am" in lowered:
            return {"type": "emotion_trigger", "notes": "Likely emotional context."}
        else:
            return {"type": "general_query", "notes": "Default assumption."}
