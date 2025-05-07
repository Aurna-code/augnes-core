import os
import json

class MemoryEngine:
    def __init__(self, storage_path="data/feedback_log.jsonl"):
        self.feedback_log = []
        self.storage_path = storage_path
        self._load_from_disk()

    def store_feedback(self, feedback: dict):
        self.feedback_log.append(feedback)
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback) + "\n")

    def _load_from_disk(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self.feedback_log = [json.loads(line) for line in f if line.strip()]

    def retrieve(self, query: str, top_k: int = 3):
        results = []
        for fb in self.feedback_log:
            goal = fb.get("goal", {}).get("goal_summary", "").lower()
            if query.lower() in goal:
                results.append(fb)
        return results[:top_k]