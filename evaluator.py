# evaluator.py

class Evaluator:
    def __init__(self, llm):
        self.llm = llm

    def evaluate_change(self, before_behavior: str, after_behavior: str) -> bool:
        prompt = f"""
You are evaluating an agent change.

BEFORE CHANGE BEHAVIOR:
{before_behavior}

AFTER CHANGE BEHAVIOR:
{after_behavior}

Question:
Did the change improve clarity, correctness, or goal achievement?

Respond ONLY with YES or NO.
"""
        verdict = self.llm(prompt).strip().upper()
        return verdict == "YES"
