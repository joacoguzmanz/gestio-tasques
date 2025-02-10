from managers.task_manager import TaskManager
from models.tasks import Task
from datetime import datetime

if __name__ == "__main__":
    t_manager = TaskManager()
    t_manager.list_projects()

    new_task = Task(title="Test Task 1", description="This is a test task", priority=1, due_date=datetime.now())
    other_task = Task(title="Some new task", description="This is a other task", priority=1, due_date=datetime.now())

    prat_project = t_manager.create_project("Prat")
    print("Show projects")
    t_manager.list_projects()
    print("\nProjects in Prat")
    t_manager.list_tasks_in_project(prat_project)
    print("--------")
    t_manager.add_task_to_project("", new_task)
    print("\nUpdate projects in Prat")
    t_manager.add_task_to_project(prat_project, other_task)
    t_manager.list_tasks_in_project(prat_project)
    t_manager.list_tasks_in_project(list(t_manager.projects.values())[0].uuid)
    print("--------")
    print(t_manager.get_task_details(other_task.uuid))
    t_manager.remove_task_from_project(prat_project, other_task.uuid)
    t_manager.list_tasks_in_project(prat_project)
    # t_manager.add_task_to_project(other_task)

