# memory.py
import json
from datetime import datetime

class Memory:
    def __init__(self, path="memory.json"):
        self.path = path
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {
                "goal": "",
                "history": []
            }

    def set_goal(self, goal: str):
        self.data["goal"] = goal
        self._save()

    def add(self, entry_type: str, content: str):
        self.data["history"].append({
            "type": entry_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()

    def get_history(self):
        return self.data["history"]

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)
