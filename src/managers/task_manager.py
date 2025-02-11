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
        self._undo_stack: List[Dict] = []
        self._redo_stack: List[Dict] = []

        inbox = Project("Inbox")
        self.projects[inbox.uuid] = inbox

    def _save_state(self) -> None:
        state = {
            "projects": {project.uuid: project.__dict__ for project in self.projects.values()}
        }
        self._undo_stack.append(state)
        self._redo_stack.clear()

# def _restore_state(self) -> None:
#     self.projects = {}
#     for project_uuid, project_data in state["projects"].items():
#         project = Project(project_data["name"])
#         project.uuid = project_uuid
#         project.tasks = [Task(**task_data) for task_data in project_data["tasks"]]
#         self.projects[project_uuid] = project*/}

    def create_project(self, project_name: str) -> str:
        for project in self.projects.values():
            if project.name == project_name:
                print(f"⚠️ El proyecto '{project_name}' ya existe con ID {project.uuid}.")
                return project.uuid  # Devuelve el ID del proyecto existente

        # Si no existe, lo crea
        project = Project(project_name)
        self.projects[project.uuid] = project
        print(f"✅ Proyecto '{project_name}' creado con ID {project.uuid}.")
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
    
    def get_project_id_by_name(self, project_name: str) -> Optional[str]:
        for project_id, project in self.projects.items():
            if project.name == project_name:
                return project_id
        print(f"❌ Proyecto '{project_name}' no encontrado.")
        return None  # Devuelve None si no se encuentra


    def get_tasks_by_priority(self, priority: int) -> List[str]:
        matching_tasks = []

        for project in self.projects.values():
            for task in project.tasks:
                if task.priority == priority:
                    matching_tasks.append(task.uuid)

        return matching_tasks

    def get_tasks_by_project(self, project_id: str) -> List[str]:
        if project_id in self.projects:
            print(project_id)
            print(self.projects)
            return [task.uuid for task in self.projects[project_id].tasks]
        else:
            print(f"Project '{project_id}' not found.")
            return []

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for project in self.projects.values():
            all_tasks.extend(project.tasks)
        return all_tasks
    
    def get_all_task_ids(self) -> List[str]:
        return [task.uuid for project in self.projects.values() for task in project.tasks]

    def get_tasks_sorted_by_priority(self) -> List[Task]:
        all_tasks = self.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.priority)

    def sort_tasks_ids_by_priority(self, task_ids: List[str]) -> List[str]:
        all_tasks = self.get_all_tasks()
        task_map = {task.uuid: task for task in all_tasks}
        sorted_tasks = sorted(
            [task_map[task_id] for task_id in task_ids if task_id in task_map],
            key=lambda t: t.priority
        )
        return [task.uuid for task in sorted_tasks]

    def get_all_task_ids_sorted_by_due_date(self) -> List[str]:
        return [
            task.uuid
            for task in sorted(
                (task for project in self.projects.values() for task in project.tasks),
                key=lambda t: t.due_date if t.due_date else datetime.max  # Tareas sin fecha van al final
            )
        ]