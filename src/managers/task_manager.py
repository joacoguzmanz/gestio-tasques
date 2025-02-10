from datetime import datetime
from typing import Dict, List, Optional
from models.projects import Project
from models.tasks import Task

class TaskManager:
    _instance = None

    @staticmethod
    def get_instance():
        if TaskManager._instance is None:
            TaskManager._instance = TaskManager()
        return TaskManager._instance

    def __init__(self) -> None:
        """Initialize the Task Manager with an empty dictionary of projects."""
        self.projects: Dict[str, Project] = {}

        inbox = Project("Inbox")
        self.projects[inbox.uuid] = inbox

    def create_project(self, project_name: str) -> str:
        project = Project(project_name)
        self.projects[project.uuid] = project
        print(f"Project '{project_name}' created with ID {project.uuid}.")
        return project.uuid

    def delete_project(self, project_id: str) -> bool:
        if project_id in self.projects:
            del self.projects[project_id]
            print(f"Project '{project_id}' deleted.")
            return True
        else:
            print(f"Project '{project_id}' not found.")
            return False

    def add_task_to_project(self, project_id: str, task: Task) -> None:
        if not project_id or project_id not in self.projects:
            project_id = list(self.projects.values())[0].uuid
        self.projects[project_id].add_task(task)
        print(f"Task '{task.title}' added to project '{self.projects[project_id].name}' (ID: {project_id}).")

    def remove_task_from_project(self, project_id: str, task_id: str) -> bool:
        if project_id in self.projects:
            success = self.projects[project_id].remove_task(task_id)
            if success:
                print(f"Task '{task_id}' removed from project '{self.projects[project_id].name}'.")
            else:
                print(f"Task '{task_id}' not found in project '{self.projects[project_id].name}'.")
            return success
        else:
            print(f"Project '{project_id}' not found.")
            return False

    def list_projects(self) -> None:
        if not self.projects:
            print("No projects available.")
        else:
            print("Projects:")
            for project in self.projects.values():
                print(f"- {project.name} (ID: {project.uuid})")

    def list_tasks_in_project(self, project_id: str) -> None:
        if project_id in self.projects:
            self.projects[project_id].list_tasks()
        else:
            print(f"Project '{project_id}' not found.")

    def get_tasks_due_today(self) -> list[str]:
        today = datetime.now().date()
        due_today = []

        for project in self.projects.values():
            for task in project.tasks:
                if task.due_date and isinstance(task.due_date, datetime):
                    if task.due_date.date() == today:
                        due_today.append(task.uuid)
                elif task.due_date == today:
                    due_today.append(task.uuid)
        return due_today

    def get_task_details(self, task_id: str) -> Optional[dict]:
        for project in self.projects.values():
            for task in project.tasks:
                if task.uuid == task_id:
                    return {
                        "project": project.name,
                        "project_uuid": project.uuid,
                        "uuid": task.uuid,
                        "title": task.title,
                        "description": task.description,
                        "priority": task.priority,
                        "state": task.state,
                        "due_date": task.due_date.strftime("%Y-%m-%d %H:%M:%S") if task.due_date else "No due date",
                        "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    }

        print(f"Task with ID '{task_id}' not found.")
        return None

    def get_tasks_by_priority(self, priority: int) -> List[str]:
        matching_tasks = []

        for project in self.projects.values():
            for task in project.tasks:
                if task.priority == priority:
                    matching_tasks.append(task.uuid)

        return matching_tasks

    def get_tasks_by_project(self, project_id: str) -> List[str]:
        if project_id in self.projects:
            return [task.uuid for task in self.projects[project_id].tasks]
        else:
            print(f"Project '{project_id}' not found.")
            return []


