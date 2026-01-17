# critic.py

class Critic:
    def __init__(self, llm):
        self.llm = llm

    def review(self, goal: str, result: str) -> str:
        prompt = f"""
You are a strict critic.

GOAL:
{goal}

OUTPUT / RESULT:
{result}

Your job:
- Identify flaws, gaps, or weak reasoning
- Suggest what should be improved next
- If result is excellent and complete, say ACCEPT

Be concise and honest.
"""
        return self.llm(prompt)
