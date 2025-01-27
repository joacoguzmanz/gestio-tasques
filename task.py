class Task:
    def __init__(self, title, description, due_date, priority, created_at) -> None:
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.created_at = created_at

    def show_task(self):
        print(f"Title: {self.title} | Desc: {self.description} | Due date: {self.due_date} | Priority: {self.priority}")

class ListTask:
    def __init__(self) -> None:
        self.task_list = []

    def add_task(self, task) -> None:
        self.task_list.append(task)

    def show_tasks(self):
        for task in self.task_list:
            print(task.title)
