from datetime import datetime
from typing import Dict, List, Optional
from models.projects import Project
from models.tasks import Task

class TaskManager:
    def __init__(self) -> None:
        """Initialize the Task Manager with an empty dictionary of projects."""
        self.projects: Dict[str, Project] = {"Inbox": Project("Inbox")}

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

    def add_task_to_project(self, task: Task, project_name: str="Inbox") -> None:
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

    def get_tasks_due_today(self) -> list[str]:
        today = datetime.now().date()
        due_today = []

        for project in self.projects.values():
            for task in project.tasks:
                if task.due_date and task.due_date.date() == today:
                    due_today.append(task.uuid)

        return due_today

    def get_task_details(self, task_id: str) -> Optional[dict]:
        for project_name, project in self.projects.items():
            for task in project.tasks:
                if task.uuid == task_id:
                    return {
                        "project": project_name,
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

    def get_tasks_by_project(self, project_name: str) -> List[str]:
        if project_name in self.projects:
            return [task.uuid for task in self.projects[project_name].tasks]
        else:
            print(f"Project '{project_name}' not found.")
            return []


