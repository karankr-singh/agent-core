# scheduler.py
import json
import time
from datetime import datetime

class Scheduler:
    def __init__(self, path="schedule.json"):
        self.path = path
        try:
            with open(self.path, "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

    def add_task(self, goal: str, interval_seconds: int):
        task = {
            "goal": goal,
            "interval": interval_seconds,
            "last_run": None,
            "created_at": datetime.utcnow().isoformat()
        }
        self.tasks.append(task)
        self._save()

    def due_tasks(self):
        now = time.time()
        due = []
        for task in self.tasks:
            if task["last_run"] is None:
                due.append(task)
            else:
                last = task["last_run"]
                if now - last >= task["interval"]:
                    due.append(task)
        return due

    def mark_ran(self, task):
        task["last_run"] = time.time()
        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.tasks, f, indent=2)
