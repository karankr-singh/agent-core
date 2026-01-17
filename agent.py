# agent.py
import json

class Agent:
    def __init__(self, llm, memory, long_term_memory, vector_memory, tools):
        self.llm = llm
        self.memory = memory
        self.long_term_memory = long_term_memory
        self.vector_memory = vector_memory
        self.tools = tools

    def plan(self) -> str:
        semantic_context = self.vector_memory.search(
            self.memory.data["goal"]
        )

        lessons = self.long_term_memory.get_lessons()

        prompt = f"""
You are an autonomous agent.

GOAL:
{self.memory.data['goal']}

RELEVANT PAST IDEAS (semantic memory):
{semantic_context}

PAST RUN LESSONS:
{lessons}

CURRENT RUN HISTORY:
{self.memory.get_history()}

Based on all context above,
decide the SINGLE best next step.
Be specific and actionable.
"""
        response = self.llm(prompt)
        self.memory.add("plan", response)
        return response

    def act(self, plan: str) -> str:
        prompt = f"""
Choose ONE tool and arguments.

AVAILABLE TOOLS:
1. think(text)
2. write_file(filename, content)

INSTRUCTION:
{plan}

Respond ONLY in valid JSON:
{{
  "tool": "<tool_name>",
  "args": {{ "...": "..." }}
}}
"""
        decision_raw = self.llm(prompt)

        try:
            decision = json.loads(decision_raw)
            tool = decision["tool"]
            args = decision["args"]

            if tool not in self.tools:
                raise ValueError(f"Unknown tool: {tool}")

            result = self.tools[tool](**args)

        except Exception as e:
            result = f"Tool execution failed: {e}"

        self.memory.add("action", {
            "plan": plan,
            "decision": decision_raw,
            "result": result
        })

        return result

    def reflect(self, result: str, critic) -> str:
        critique = critic.review(
            goal=self.memory.data["goal"],
            result=result
        )

        self.memory.add("critic_feedback", critique)

        if "ACCEPT" in critique.upper():
            self.long_term_memory.add_lesson(
                f"Successful strategy for goal '{self.memory.data['goal']}'."
            )
            self.vector_memory.add(
                f"Successful completion pattern: {result}"
            )
            decision = "DONE"
        else:
            lesson = f"For goal '{self.memory.data['goal']}', improvement needed: {critique}"
            self.long_term_memory.add_lesson(lesson)
            decision = f"CONTINUE: {critique}"

        self.memory.add("reflection", decision)
        return decision
