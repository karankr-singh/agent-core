# code_sandbox.py
import ast
import os

class CodeSandbox:
    def __init__(self, allowed_files):
        self.allowed_files = allowed_files

    def validate_python(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def apply_patch(self, filename: str, new_code: str) -> str:
        if filename not in self.allowed_files:
            raise PermissionError("File modification not allowed")

        if not self.validate_python(new_code):
            raise ValueError("Invalid Python syntax")

        with open(filename, "w") as f:
            f.write(new_code)

        return f"Updated {filename} successfully"
