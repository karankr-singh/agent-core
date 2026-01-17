# rollback_manager.py
import shutil
import os
from datetime import datetime

class RollbackManager:
    def __init__(self, backup_dir=".backups"):
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup(self, filename: str):
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        backup_path = os.path.join(
            self.backup_dir, f"{filename}.{ts}.bak"
        )
        shutil.copyfile(filename, backup_path)
        return backup_path

    def restore(self, backup_path: str, filename: str):
        shutil.copyfile(backup_path, filename)
        return f"Rolled back {filename}"
