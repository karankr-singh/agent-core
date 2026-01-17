# message_bus.py
import json
import time
from pathlib import Path

class MessageBus:
    def __init__(self, path="bus"):
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)

    def publish(self, topic: str, message: dict):
        fname = self.path / f"{topic}.jsonl"
        with open(fname, "a") as f:
            f.write(json.dumps({
                "ts": time.time(),
                "msg": message
            }) + "\n")

    def consume(self, topic: str, last_ts: float = 0.0):
        fname = self.path / f"{topic}.jsonl"
        if not fname.exists():
            return [], last_ts

        out = []
        new_last = last_ts
        with open(fname, "r") as f:
            for line in f:
                obj = json.loads(line)
                if obj["ts"] > last_ts:
                    out.append(obj["msg"])
                    new_last = max(new_last, obj["ts"])
        return out, new_last
