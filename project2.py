import json
import os

TASKS_FILE = 'tasks.json'

class Task:
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {'id': self.id, 'description': self.description, 'completed': self.completed}

    @staticmethod
    def from_dict(data):
        return Task(data['id'], data['description'], data['completed'])

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as file:
                try:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(task) for task in data]
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
                except json.JSONDecodeError:
                    print("Error: Corrupted tasks file. Starting with an empty task list.")
                    self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, description):
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        print(f"Task added with ID {task.id}.")

    def edit_task(self, task_id, new_description):
        task = self.find_task(task_id)
        if task:
            task.description = new_description
            self.save_tasks()
            print(f"Task {task_id} has been updated.")
        else:
            print(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"Task {task_id} has been deleted.")
        else:
            print(f"Task with ID {task_id} not found.")

    def mark_complete(self, task_id):
        task = self.find_task(task_id)
        if task:
            task.completed = True
            self.save_tasks()
            print(f"Task {task_id} marked as complete.")
        else:
            print(f"Task with ID {task_id} not found.")

    def mark_incomplete(self, task_id):
        task = self.find_task(task_id)
        if task:
            task.completed = False
            self.save_tasks()
            print(f"Task {task_id} marked as incomplete.")
        else:
            print(f"Task with ID {task_id} not found.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks to display.")
            return
        print("\nCurrent Tasks:")
        print("{:<5} {:<50} {:<10}".format("ID", "Description", "Status"))
        print("-" * 70)
        for task in self.tasks:
            status = "Complete" if task.completed else "Incomplete"
            print("{:<5} {:<50} {:<10}".format(task.id, task.description, status))
        print()

    def find_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

def display_menu():
    print("\n=== Task Manager ===")
    print("1. List Tasks")
    print("2. Add Task")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Mark Task as Complete")
    print("6. Mark Task as Incomplete")
    print("7. Exit")

def main():
    manager = TaskManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            manager.list_tasks()
        elif choice == '2':
            description = input("Enter task description: ").strip()
            if description:
                manager.add_task(description)
            else:
                print("Task description cannot be empty.")
        elif choice == '3':
            try:
                task_id = int(input("Enter the ID of the task to edit: "))
                new_description = input("Enter the new description: ").strip()
                if new_description:
                    manager.edit_task(task_id, new_description)
                else:
                    print("New description cannot be empty.")
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif choice == '4':
            try:
                task_id = int(input("Enter the ID of the task to delete: "))
                manager.delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif choice == '5':
            try:
                task_id = int(input("Enter the ID of the task to mark as complete: "))
                manager.mark_complete(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif choice == '6':
            try:
                task_id = int(input("Enter the ID of the task to mark as incomplete: "))
                manager.mark_incomplete(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif choice == '7':
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 7.")

if __name__ == "__main__":
    main()
