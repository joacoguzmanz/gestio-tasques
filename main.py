import task

if __name__ == "__main__":
    my_tasks = task.ListTask()
    new_task = task.Task("Comer", "28/01", "high", "27/01", "Probando")
    other_task = task.Task("Dormir", "28/01", "high", "27/01", "Otra prueba")

    my_tasks.add_task(new_task)
    my_tasks.add_task(other_task)

    my_tasks.show_tasks()

