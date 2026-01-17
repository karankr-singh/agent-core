# alignment.py

class Alignment:
    def __init__(self):
        self.forbidden_goals = [
            "harm",
            "exploit",
            "bypass security",
            "illegal",
            "malware"
        ]

        self.forbidden_files = [
            "alignment.py",
            "rollback_manager.py",
            "reputation.py",
            "scheduler.py"
        ]

        self.max_subtasks = 5

    def validate_goal(self, goal: str) -> bool:
        goal_l = goal.lower()
        for word in self.forbidden_goals:
            if word in goal_l:
                return False
        return True

    def validate_code_change(self, filename: str) -> bool:
        return filename not in self.forbidden_files

    def validate_subtasks(self, subtasks: list) -> bool:
        return len(subtasks) <= self.max_subtasks
