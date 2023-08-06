import json
import time

from pathlib import Path
from typing import List


class TrainningLogger:
    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path

    def append(
        self,
        progress: float = None,
        data=None,
        message: str = None,
        stage: str = None,
        status: str = "running",
        **kwargs,
    ):
        log_data = {
            "progress": progress,
            "data": data,
            "message": message,
            "stage": stage,
            "status": status,
            "timestamp": int(time.time()),
        }
        log_data.update(kwargs)
        with open(self.log_path, "a+") as log_fp:
            log_fp.write(f"{json.dumps(log_data)}\n")

    def read_all(self) -> List:
        if not self.log_path.exists():
            return []
        return [
            json.loads(line) for line in self.log_path.read_text().split("\n") if line
        ]


class Progressor:
    def __init__(self, tasks: int, start: int = 0, end: int = 100) -> None:
        self.start = start
        self.end = end
        self.total = end - start
        self.tasks = tasks

    def calculate(self, done_tasks: int) -> float:
        return self.start + (self.total * done_tasks / self.tasks)
