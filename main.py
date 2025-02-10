from datetime import datetime
from src.models.tasks import Task

if __name__ == "__main__":
    # Example without a due date.
    task1 = Task("Buy groceries", "Milk, eggs, bread", priority=2)

    # Example with a due date.
    due = datetime(2025, 2, 15, 17, 0)  # Example due date: Feb 15, 2025 at 17:00
    task2 = Task("Write report", "Complete the annual report", priority=1, due_date=due)

    print(task1)
    print(task2)

    # Mark task1 as done and display its updated state.
    task1.mark_done()
    print("After marking task1 done:")
    print(task1)

