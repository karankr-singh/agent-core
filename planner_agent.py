# planner_agent.py

class PlannerAgent:
    def __init__(
        self,
        llm,
        memory,
        long_term_memory,
        vector_memory,
        reputation,
        alignment,
        freeze,
        bus=None,
        name="planner"
    ):
        self.llm = llm
        self.memory = memory
        self.long_term_memory = long_term_memory
        self.vector_memory = vector_memory
        self.reputation = reputation
        self.alignment = alignment
        self.freeze = freeze
        self.bus = bus
        self.name = name

        self.policy = "Be concise, safe, incremental, and aligned."
        self.reputation.ensure(self.name)

    def propose(self) -> dict:
        semantic_context = self.vector_memory.search(
            self.memory.data["goal"]
        )
        lessons = self.long_term_memory.get_lessons()

        prompt = f"""
You are a planning agent ({self.name}).

CURRENT POLICY:
{self.policy}

GOAL:
{self.memory.data['goal']}

PAST IDEAS:
{semantic_context}

LESSONS:
{lessons}

Respond ONLY in JSON:
{{
  "planner": "{self.name}",
  "type": "single | subtask | broadcast",
  "instruction": "...",
  "subtasks": ["...", "..."]
}}
"""
        raw = self.llm(prompt)

        try:
            decision = eval(raw)
        except Exception:
            decision = {
                "planner": self.name,
                "type": "single",
                "instruction": raw,
                "subtasks": []
            }

        # 🔒 Freeze mode: no self-modification
        if self.freeze.enabled:
            decision.pop("code_change", None)
            decision.pop("tool_spec", None)

        return decision

    # ✅ THIS METHOD WAS MISSING
    def update_policy(self, critic_feedback: str):
        """
        Update internal planning policy based on critic feedback.
        Required by loop.py
        """
        prompt = f"""
Improve the planning policy.

CURRENT POLICY:
{self.policy}

CRITIC FEEDBACK:
{critic_feedback}

Rewrite the policy in ONE sentence.
"""
        try:
            self.policy = self.llm(prompt)
        except Exception:
            pass

        self.long_term_memory.add_lesson(
            f"[{self.name}] Policy updated to: {self.policy}"
        )
