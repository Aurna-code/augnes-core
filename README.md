
# Augnes Core (MVP v0.1)

This is the MVP version of the **Augnes Core FSM System**, featuring:

- 🧠 Goal → Intent → Self-Regulation → Execution flow
- 📦 Feedback persistence to disk (JSONL)
- ❌ Constraint-based blocking via external YAML rules
- 🔍 CLI-based RAG-style keyword retrieval from past interactions

## 📂 Structure

```
augnes-core/
├── core/               # DOCFSM: Main logic flow
├── memory/             # MemoryEngine: Feedback storage & retrieval
├── scripts/            # CLI entrypoint
├── configs/            # Regulation rule config
├── tests/              # Pytest unit tests
├── data/               # Feedback logs (ignored from git)
```

## 🚀 How to Run

```bash
export PYTHONPATH="$HOME/augnes-core"
python3 scripts/entry.py
```

Use `!search <keyword>` to retrieve past goals by keyword.

## ✅ Requirements

```bash
pip install -r requirements.txt
```

## 🛡️ Safety Layer

All goal-intent pairs are evaluated against `configs/self_regulate_rules.yaml` before execution.
