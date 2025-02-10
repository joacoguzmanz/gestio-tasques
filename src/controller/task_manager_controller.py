from managers.task_manager import TaskManager

# If the function does not return anything
def create_project_controller(project_name):
    task_manager = TaskManager()
    task_manager.create_project(project_name)

# If the function returns something
def delete_project_controller(project_name):
    task_manager = TaskManager()
    return task_manager.delete_project(project_name)