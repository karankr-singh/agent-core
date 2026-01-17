# long_term_memory.py
import json
from datetime import datetime

class LongTermMemory:
    def __init__(self, path="long_term_memory.json"):
        self.path = path
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def add_lesson(self, lesson: str):
        self.data.append({
            "lesson": lesson,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save()

    def get_lessons(self, limit=5):
        return self.data[-limit:]

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)
