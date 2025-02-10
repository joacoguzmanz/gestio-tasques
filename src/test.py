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
    work_p = t_manager.create_project("Work")

    # List projects
    print("\n--------\n")
    t_manager.list_projects()
    print("\n--------\n")

    # Add tasks to projects randomly
    for task in gen_tasks:
        project_id = choice([prat_p, work_p])  # Randomly choose a project
        t_manager.add_task_to_project(project_id, task)

    # List tasks in both projects
    print("\nTasks in 'Prat' project:")
    t_manager.list_tasks_in_project(prat_p)

    print("\nTasks in 'Work' project:")
    t_manager.list_tasks_in_project(work_p)

    # Test get_tasks_due_today
    tasks_due_today = t_manager.get_tasks_due_today()
    print("\n--------\n")
    print("Tasks due today:")
    for task_uuid in tasks_due_today:
        task_details = t_manager.get_task_details(task_uuid)
        if task_details:
            print(f"- {task_details['title']} (ID: {task_uuid}, Due: {task_details['due_date']})")

    # Test get_tasks_sorted_by_priority
    sorted_tasks = t_manager.get_tasks_sorted_by_priority()
    print("\n--------\n")
    print("Tasks sorted by priority:")
    for task in sorted_tasks:
        print(f"- {task.title} (Priority: {task.priority})")

    # Test get_all_tasks
    all_tasks = t_manager.get_all_tasks()
    print("\n--------\n")
    print("All tasks across all projects:")
    for task in all_tasks:
        print(f"- {task.title} (Priority: {task.priority})")
