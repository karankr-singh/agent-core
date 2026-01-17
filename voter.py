# voter.py

class Voter:
    def __init__(self, llm, reputation):
        self.llm = llm
        self.reputation = reputation

    def choose(self, goal: str, proposals: list) -> dict:
        weighted = []
        for i, p in enumerate(proposals):
            planner = p.get("planner", "unknown")
            score = self.reputation.get(planner)
            weighted.append((i, planner, score, p))

        prompt = f"""
You are a decision arbiter.

GOAL:
{goal}

PLANS WITH TRUST SCORES:
{weighted}

Choose the BEST plan.
Respond ONLY with the INDEX of the chosen plan.
"""
        idx = self.llm(prompt).strip()
        try:
            idx = int(idx)
            return proposals[idx]
        except Exception:
            return proposals[0]
