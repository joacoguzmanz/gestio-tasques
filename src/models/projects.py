import uuid
from typing import List
from models.tasks import Task

class Project:
    def __init__(self, name: str) -> None:
        """
        Initialize a new project.

        Args:
            name (str): The name of the project.
        """
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.tasks: List[Task] = []

    def __str__(self) -> str:
        return f"Project(ID: {self.uuid}, Name: {self.name}, Tasks: {len(self.tasks)})"

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        for task in self.tasks:
            if task.uuid == task_id:
                self.tasks.remove(task)
                return True
        return False

    def list_tasks(self) -> None:
        print(f"Tasks for project '{self.name}':")
        for task in self.tasks:
            print(task)

    def get_tasks_by_priority(self) -> List[Task]:
        return sorted(self.tasks, key=lambda t: t.priority)
