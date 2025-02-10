from managers.task_manager import TaskManager
from models.tasks import Task

# If the function does not return anything
def create_project_controller(project_name):
    task_manager = TaskManager()
    task_manager.create_project(project_name)

# If the function returns something
def delete_project_controller(project_name):
    task_manager = TaskManager()
    return task_manager.delete_project(project_name)

def add_task_to_project_controller(project_id: str, task: Task):
    task_manager = TaskManager()
    task_manager.add_task_to_project(project_id, task)

    from managers.task_manager import TaskManager

def remove_task_from_project_controller(project_id: str, task_id: str) -> bool:
    task_manager = TaskManager()
    return task_manager.remove_task_from_project(project_id, task_id)

from managers.task_manager import TaskManager

def list_projects_controller():
    task_manager = TaskManager()
    task_manager.list_projects()


from managers.task_manager import TaskManager

def list_tasks_in_project_controller(project_id: str):
    task_manager = TaskManager()
    task_manager.list_tasks_in_project(project_id)

from managers.task_manager import TaskManager

def get_tasks_due_today_controller() -> list:
    task_manager = TaskManager()
    return task_manager.get_tasks_due_today()

from managers.task_manager import TaskManager

def get_task_details_controller(task_id: str) -> dict:
    task_manager = TaskManager()
    return task_manager.get_task_details(task_id)

from managers.task_manager import TaskManager

def get_tasks_by_priority_controller(priority: int) -> list:
    task_manager = TaskManager()
    return task_manager.get_tasks_by_priority(priority)

from managers.task_manager import TaskManager

def get_tasks_by_project_controller(project_id: str) -> list:
    task_manager = TaskManager()
    return task_manager.get_tasks_by_project(project_id)
