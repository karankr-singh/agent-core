# executor_agent.py
import json

class ExecutorAgent:
    def __init__(self, llm, tool_registry, memory):
        self.llm = llm
        self.tool_registry = tool_registry
        self.memory = memory

    def execute(self, instruction: str) -> str:
        tools_desc = self.tool_registry.list_tools()

        prompt = f"""
You are an execution agent.

AVAILABLE TOOLS:
{tools_desc}

TASK:
{instruction}

Respond ONLY in valid JSON:
{{
  "tool": "<tool_name>",
  "args": {{ "...": "..." }}
}}
"""
        raw = self.llm(prompt)

        try:
            decision = json.loads(raw)
            result = self.tool_registry.execute(
                decision["tool"],
                **decision["args"]
            )
        except Exception as e:
            result = f"Execution failed: {e}"

        self.memory.add("execution", {
            "instruction": instruction,
            "decision": raw,
            "result": result
        })

        return result
