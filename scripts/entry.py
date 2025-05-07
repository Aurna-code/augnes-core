from core.doc_fsm import DOCFSM
from memory.rag import MemoryEngine

class DummyExecutor:
    def act(self, action_dict):
        print("⚙️ Executor Executing:", action_dict)
        return f"Executed intent '{action_dict['intent_type']}'"

if __name__ == "__main__":
    memory = MemoryEngine()
    fsm = DOCFSM(memory=memory, executor=DummyExecutor())

    while True:
        user_input = input("\n👤 You (or !search <keyword>): ")

        # 검색 명령
        if user_input.startswith("!search "):
            query = user_input.replace("!search ", "")
            results = memory.retrieve(query)
            print(f"🔍 Retrieved {len(results)} results:")
            for r in results:
                print("•", r.get("goal", {}).get("goal_summary", "N/A"))
            continue

        if user_input.lower() in ["exit", "quit"]:
            break

        result = fsm.process(user_input)
        print("📤 Output:", result)
