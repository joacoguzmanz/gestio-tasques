from typing import Dict
from models.projects import Project
from task import Task

class TaskManager:
    def __init__(self) -> None:
        """Initialize the Task Manager with an empty dictionary of projects."""
        self.projects: Dict[str, Project] = {}

    def create_project(self, project_name: str) -> None:
        if project_name in self.projects:
            print(f"Project '{project_name}' already exists.")
        else:
            self.projects[project_name] = Project(project_name)
            print(f"Project '{project_name}' created.")

    def delete_project(self, project_name: str) -> bool:
        if project_name in self.projects:
            del self.projects[project_name]
            print(f"Project '{project_name}' deleted.")
            return True
        else:
            print(f"Project '{project_name}' not found.")
            return False

    def add_task_to_project(self, project_name: str, task: Task) -> None:
        if project_name not in self.projects:
            print(f"Project '{project_name}' does not exist. Creating it now.")
            self.create_project(project_name)
        self.projects[project_name].add_task(task)
        print(f"Task '{task.title}' added to project '{project_name}'.")

    def remove_task_from_project(self, project_name: str, task_id: str) -> bool:
        if project_name in self.projects:
            success = self.projects[project_name].remove_task(task_id)
            if success:
                print(f"Task '{task_id}' removed from project '{project_name}'.")
            else:
                print(f"Task '{task_id}' not found in project '{project_name}'.")
            return success
        else:
            print(f"Project '{project_name}' not found.")
            return False

    def list_projects(self) -> None:
        if not self.projects:
            print("No projects available.")
        else:
            print("Projects:")
            for project_name in self.projects.keys():
                print(f"- {project_name}")

    def list_tasks_in_project(self, project_name: str) -> None:
        if project_name in self.projects:
            self.projects[project_name].list_tasks()
        else:
            print(f"Project '{project_name}' not found.")
