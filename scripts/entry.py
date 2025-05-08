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
    print("📂 JML PATH:", fsm.jml.path)
    print("🔄 Augnes Judgment System (CLI Ready)")

    # (선택) Preload 삭제 or 보완 주석 처리
    # from memory.jml import JudgmentMemoryEntry, StrategyResult
    # preload_entry = ...
    # fsm.jml.save(preload_entry)

    while True:
        try:
            user_input = input("\n💬 Input your task: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                break

            result = fsm.process(user_input)
            print("🎯 Final Response:", result["response"]["message"])
            print("📌 Intent Info:", result["intent"])
        except Exception as e:
            print("❌ Error:", e)
