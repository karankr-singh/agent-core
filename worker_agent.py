# worker_agent.py
from time import sleep

class WorkerAgent:
    def __init__(self, name, executor, bus):
        self.name = name
        self.executor = executor
        self.bus = bus
        self.cursor = 0.0

    def run_once(self):
        tasks, self.cursor = self.bus.consume("workers", self.cursor)
        for task in tasks:
            instruction = task.get("task", "")
            result = self.executor.execute(instruction)
            self.bus.publish(
                "results",
                {
                    "worker": self.name,
                    "instruction": instruction,
                    "result": result
                }
            )

    def loop(self, interval=1.0):
        while True:
            self.run_once()
            sleep(interval)
