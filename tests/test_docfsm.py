# entry.py — Augnes main CLI entry point

from core.doc_fsm import DOCFSM
from memory.jml import JMLManager
from datetime import datetime, timezone

# 더미 메모리와 실행기
class DummyMemory:
    def store_feedback(self, feedback):
        print("📝 Feedback stored:", feedback)

class DummyExecutor:
    def act(self, intent):
        return {
            "message": f"📌 Executed intent with strategy: {intent.get('strategy_hint', 'default')}"
        }

if __name__ == "__main__":
    fsm = DOCFSM(memory=DummyMemory(), executor=DummyExecutor())
fsm.jml = JMLManager(path="judgments.jsonl")
print("📂 JML PATH:", fsm.jml.path)

# --- optional preloading (for CLI test) ---
from memory.jml import JudgmentMemoryEntry, StrategyResult
from datetime import timezone

preload_entry = JudgmentMemoryEntry(
    domain="general",
    task_id="cli_bootstrap",
    strategies_tested=[
        StrategyResult(name="RL", success_rate=0.7, reward_avg=0.5)
    ],
    final_decision="RL",
    confidence=0.9,
    context_features={"symbolic_depth": 0.0, "sequence_length": 0.0},
    timestamp=datetime.now(timezone.utc).isoformat(),
    meta_comment="Preloaded for CLI test"
)
fsm.jml.save(preload_entry)
print("🔄 Augnes Judgment System (CLI)")
    
while True:
        try:
            user_input = input("\n💬 Input your task: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                break

            result = fsm.process(user_input)
            print("🎯 Final Response:", result["response"]["message"])
        except Exception as e:
            print("❌ Error:", e)
