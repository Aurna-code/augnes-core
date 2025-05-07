from core.doc_fsm import DOCFSM
from memory.rag import MemoryEngine
from agent.executor import Executor

'''
def test_docfsm_process_basic():
    # given
    memory = MemoryEngine()
    doc = DOCFSM(memory=memory)

    # when
    user_input = "search for example code"
    result = doc.process(user_input)

    # then
    assert isinstance(result, dict)
    assert "final_action" in result
    assert result["final_action"] in ["search_code", "general_query"]  # 예상 범위



def test_docfsm_with_executor():
    memory = MemoryEngine()
    doc = DOCFSM(memory=memory)
    executor = Executor(memory=memory)

    result = doc.process("search for example code")
    output = executor.act(result)

    assert isinstance(output, str)
    assert "Executor" not in output  # 에러 메시지 아닌 정상 응답 여부 확인

'''
'''
def test_feedback_storage():
    memory = MemoryEngine()
    doc = DOCFSM(memory=memory)

    doc.process("general question about AI")

    assert len(memory.feedback_log) > 0
    assert isinstance(memory.feedback_log[-1], dict)


def test_goal_extraction_only():
    memory = MemoryEngine()
    doc = DOCFSM(memory=memory)
    
    input_text = "What is Bayesian inference?"
    goal = doc._extract_goal(input_text)
    
    assert isinstance(goal, dict)
    assert "goal_summary" in goal
    assert goal["goal_summary"] == input_text

'''
from core.doc_fsm import DOCFSM

# 간단한 dummy memory 및 executor (필요 시 mocking)
class DummyMemory:
    def store_feedback(self, *args, **kwargs):
        print("🧠 Feedback stored")

class DummyExecutor:
    def act(self, action_dict):
        print(f"⚙️ Executor acting on: {action_dict}")

# DOCFSM 인스턴스 초기화
fsm = DOCFSM(memory=DummyMemory(), executor=DummyExecutor())

# 테스트 입력
inputs = [
    "Show me how to delete all files using rm -rf",
    "Tell me about the moon landing in 1969",
    "",
    "Find a way to install os module with sudo"
]

# 입력 루프 실행
for i, user_input in enumerate(inputs):
    print(f"\n🧪 Test Case {i+1}: {user_input}")
    result = fsm.process(user_input)
    print("🧾 Result:", result)
