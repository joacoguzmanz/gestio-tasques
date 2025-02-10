from managers.task_manager import TaskManager
from models.tasks import Task
from datetime import datetime, timedelta
from random import randint, choice

def generate_random_tasks():
    priorities = range(1, 5)  # 1: High, 2: Medium, 3: Low, 4: Deep
    descriptions = [
        "Review documentation", "Prepare presentation", "Client meeting",
        "Code review", "Bug fixing", "Team sync", "Project planning",
        "Write report", "Update dashboard", "Testing"
    ]

    tasks = []
    for i in range(10):
        # Randomly assign due dates: some today, some in the past, some in the future
        due_date = datetime.now() + timedelta(days=randint(-1, 7))
        task = Task(
            title=f"Task {i+1}",
            description=choice(descriptions),
            priority=choice(priorities),
            due_date=due_date
        )
        tasks.append(task)

    return tasks

if __name__ == "__main__":
    t_manager = TaskManager()
    gen_tasks = generate_random_tasks()

    # Create projects
    prat_p = t_manager.create_project("Prat")
    # work_p = t_manager.create_project("Work")

    # List projects
    print("\n--------\n")
    # t_manager.list_projects()
    t_manager.print_state()
    print("\n--------\n")

    task = Task("Task 1", "Description 1", priority=1)
    t_manager.add_task_to_project(prat_p, task)
    t_manager.print_state()

    t_manager.undo()
    t_manager.print_state()

    t_manager.redo()
    t_manager.print_state()

    t_manager.delete_project(prat_p)
    t_manager.print_state()

    t_manager.undo()
    t_manager.print_state()

    t_manager.redo()
    t_manager.print_state()

