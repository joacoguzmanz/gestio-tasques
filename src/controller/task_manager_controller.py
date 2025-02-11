from managers.task_manager import TaskManager
from models.tasks import Task

# If the function does not return anything
def create_project_controller(project_name):
    task_manager = TaskManager().get_instance()
    return task_manager.create_project(project_name)

def add_task_to_project_controller(project_id, title, description, priority, due_date):
    task = Task(title, description, priority, due_date)
    task_manager = TaskManager().get_instance()
    task_manager.add_task_to_project(project_id, task)

def remove_task_from_project_controller(project_id, task_id):
    task_manager = TaskManager().get_instance()
    return task_manager.remove_task_from_project(project_id, task_id)

# If the function returns something
def delete_project_controller(project_name):
    task_manager = TaskManager().get_instance()
    return task_manager.delete_project(project_name)

def list_tasks_in_project_controller(project_name):
    task_manager = TaskManager().get_instance()
    return task_manager.list_tasks_in_project(project_name)

def get_task_due_today_controller():
    task_manager = TaskManager().get_instance()
    return task_manager.get_tasks_due_today()

def get_task_details_controller(task_id):
    task_manager = TaskManager().get_instance()
    return task_manager.get_task_details(task_id)

def get_tasks_by_priority_controller(priority):
    task_manager = TaskManager().get_instance()
    return task_manager.get_tasks_by_priority(priority)

def get_project_id_by_name_controller(project_name):
    task_manager = TaskManager().get_instance()
    return task_manager.get_project_id_by_name(project_name)

def get_tasks_by_project_controller(project_name):
    task_manager = TaskManager().get_instance()
    return task_manager.get_tasks_by_project(project_name)

def get_all_tasks_controller():
    task_manager = TaskManager().get_instance()
    return task_manager.get_all_tasks()

def get_all_task_ids_controller():
    task_manager = TaskManager().get_instance()
    return task_manager.get_all_task_ids()

def sort_tasks_ids_by_priority_controller(task_ids):
    task_manager = TaskManager().get_instance()
    return task_manager.sort_tasks_ids_by_priority(task_ids)

def get_all_task_ids_sorted_by_due_date_controller():
    task_manager = TaskManager().get_instance()
    return task_manager.get_all_task_ids_sorted_by_due_date()