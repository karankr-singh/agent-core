# tool_registry.py

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, description: str, func):
        self.tools[name] = {
            "description": description,
            "func": func
        }

    def list_tools(self):
        return {
            name: meta["description"]
            for name, meta in self.tools.items()
        }

    def execute(self, name: str, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        return self.tools[name]["func"](**kwargs)
