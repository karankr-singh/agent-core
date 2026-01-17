# meta_goals.py

class MetaGoals:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, context: str) -> list:
        prompt = f"""
You are a curiosity engine.

CONTEXT:
{context}

Generate 3 useful new goals that would improve the system.
Respond ONLY as a Python list of strings.
"""
        raw = self.llm(prompt)
        try:
            goals = eval(raw)
            if isinstance(goals, list):
                return goals
        except Exception:
            pass
        return []

    def prioritize(self, goals: list) -> list:
        prompt = f"""
You are prioritizing goals.

GOALS:
{goals}

Reorder goals from highest to lowest value.
Respond ONLY as a Python list.
"""
        raw = self.llm(prompt)
        try:
            ordered = eval(raw)
            if isinstance(ordered, list):
                return ordered
        except Exception:
            pass
        return goals
