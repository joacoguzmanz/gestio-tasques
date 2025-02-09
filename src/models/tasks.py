import uuid
from datetime import datetime
from typing import Optional

class Task:
    def __init__(self, title, description, priority, due_date: Optional[datetime]=None, state="todo") -> None:
        """
        Initialize a new Task.

        Args:
            name (str): The name/title of the task.
            description (str): A brief description of the task.
            priority (int): The priority level (e.g., 1 for highest, increasing numbers for lower priority).
            state (str): The state of the task (default is "todo"). Could be "todo" or "done".
        """
        self.uuid = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.state = state
        self.created_at = datetime.now()

    def mark_done(self) -> None:
        self.state = "done"

    def mark_todo(self) -> None:
        self.state = "todo"

    def __str__(self) -> str:
        due_date_str = self.due_date.strftime("%Y-%m-%d %H:%M:%S") if self.due_date else "No due date"
        return (f"Task(ID: {self.uuid}, Name: {self.title}, Description: {self.description}, "
                f"Priority: {self.priority}, State: {self.state}, "
                f"Due: {due_date_str}, Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')})")
