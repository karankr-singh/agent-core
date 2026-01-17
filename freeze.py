# freeze.py

class Freeze:
    def __init__(self, enabled=True):
        self.enabled = enabled

    def allow_self_modification(self) -> bool:
        return not self.enabled

    def allow_meta_goals(self) -> bool:
        return not self.enabled

    def allow_tool_invention(self) -> bool:
        return not self.enabled
