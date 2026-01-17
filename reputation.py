# reputation.py

class Reputation:
    def __init__(self):
        self.scores = {}

    def ensure(self, name: str):
        if name not in self.scores:
            self.scores[name] = 1.0  # neutral trust

    def reward(self, name: str, amount: float = 0.1):
        self.ensure(name)
        self.scores[name] += amount

    def penalize(self, name: str, amount: float = 0.1):
        self.ensure(name)
        self.scores[name] = max(0.0, self.scores[name] - amount)

    def get(self, name: str) -> float:
        self.ensure(name)
        return self.scores[name]

    def snapshot(self):
        return dict(self.scores)
