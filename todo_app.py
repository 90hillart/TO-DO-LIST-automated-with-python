#!/usr/bin/env python3
"""
Simple To-Do List CRUD Application
A command-line task manager with full Create, Read, Update, Delete functionality.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class TodoList:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Dict] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load tasks from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self) -> None:
        """Save tasks to JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def create_task(self, title: str, description: str = "", priority: str = "medium") -> Dict:
        """Create a new task."""
        task = {
            "id": self._generate_id(),
            "title": title,
            "description": description,
            "priority": priority.lower(),
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def _generate_id(self) -> int:
        """Generate unique ID for new task."""
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1

    def get_all_tasks(self) -> List[Dict]:
        """Read all tasks."""
        return self.tasks

    def get_task(self, task_id: int) -> Optional[Dict]:
        """Read a specific task by ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def update_task(self, task_id: int, **kwargs) -> Optional[Dict]:
        """Update an existing task."""
        task = self.get_task(task_id)
        if not task:
            return None

        allowed_fields = ["title", "description", "priority", "completed"]
        for key, value in kwargs.items():
            if key in allowed_fields:
                task[key] = value

        task["updated_at"] = datetime.now().isoformat()
        self.save_tasks()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return True
        return False

    def toggle_complete(self, task_id: int) -> Optional[Dict]:
        """Toggle completion status of a task."""
        task = self.get_task(task_id)
        if task:
            return self.update_task(task_id, completed=not task["completed"])
        return None

    def get_stats(self) -> Dict:
        """Get task statistics."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed

        priority_count = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            p = task.get("priority", "medium")
            if p in priority_count:
                priority_count[p] += 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": priority_count
        }

def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def print_task(task: Dict, index: int = None):
    """Print a single task with formatting."""
    status = "✓" if task["completed"] else "○"
    priority_colors = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }
    priority_icon = priority_colors.get(task["priority"], "⚪")

    prefix = f"{index}. " if index else ""
    print(f"{prefix}[{status}] {priority_icon} #{task['id']}: {task['title']}")
    if task["description"]:
        print(f"     📝 {task['description']}")
    print(f"     📅 Created: {task['created_at'][:10]}")
    print()

def main():
    todo = TodoList()

    while True:
        print_header("📋 TO-DO LIST MANAGER")
        print("1. ➕  Add New Task")
        print("2. 📋  View All Tasks")
        print("3. 🔍  View Task Details")
        print("4. ✏️   Update Task")
        print("5. ✅  Toggle Complete")
        print("6. 🗑️   Delete Task")
        print("7. 📊  Statistics")
        print("0. 🚪  Exit")
        print("-" * 50)

        choice = input("Select option: ").strip()

        if choice == "1":
            print_header("➕ ADD NEW TASK")
            title = input("Title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                continue
            description = input("Description (optional): ").strip()
            priority = input("Priority (high/medium/low) [medium]: ").strip() or "medium"

            task = todo.create_task(title, description, priority)
            print(f"✅ Task created with ID: {task['id']}")

        elif choice == "2":
            print_header("📋 ALL TASKS")
            tasks = todo.get_all_tasks()
            if not tasks:
                print("No tasks found. Add some tasks first!")
            else:
                for i, task in enumerate(tasks, 1):
                    print_task(task, i)

        elif choice == "3":
            print_header("🔍 VIEW TASK")
            try:
                task_id = int(input("Enter task ID: "))
                task = todo.get_task(task_id)
                if task:
                    print_task(task)
                else:
                    print(f"❌ Task #{task_id} not found")
            except ValueError:
                print("❌ Please enter a valid number")

        elif choice == "4":
            print_header("✏️ UPDATE TASK")
            try:
                task_id = int(input("Enter task ID: "))
                task = todo.get_task(task_id)
                if not task:
                    print(f"❌ Task #{task_id} not found")
                    continue

                print(f"Current title: {task['title']}")
                new_title = input("New title (press Enter to keep): ").strip()

                print(f"Current description: {task['description']}")
                new_desc = input("New description (press Enter to keep): ").strip()

                print(f"Current priority: {task['priority']}")
                new_priority = input("New priority (high/medium/low, press Enter to keep): ").strip()

                updates = {}
                if new_title:
                    updates["title"] = new_title
                if new_desc:
                    updates["description"] = new_desc
                if new_priority:
                    updates["priority"] = new_priority

                if updates:
                    todo.update_task(task_id, **updates)
                    print("✅ Task updated successfully")
                else:
                    print("No changes made")
            except ValueError:
                print("❌ Please enter a valid number")

        elif choice == "5":
            print_header("✅ TOGGLE COMPLETE")
            try:
                task_id = int(input("Enter task ID: "))
                task = todo.toggle_complete(task_id)
                if task:
                    status = "completed" if task["completed"] else "pending"
                    print(f"✅ Task marked as {status}")
                else:
                    print(f"❌ Task #{task_id} not found")
            except ValueError:
                print("❌ Please enter a valid number")

        elif choice == "6":
            print_header("🗑️ DELETE TASK")
            try:
                task_id = int(input("Enter task ID: "))
                confirm = input(f"Are you sure you want to delete task #{task_id}? (y/n): ").lower()
                if confirm == 'y':
                    if todo.delete_task(task_id):
                        print("✅ Task deleted successfully")
                    else:
                        print(f"❌ Task #{task_id} not found")
                else:
                    print("Deletion cancelled")
            except ValueError:
                print("❌ Please enter a valid number")

        elif choice == "7":
            print_header("📊 STATISTICS")
            stats = todo.get_stats()
            print(f"Total tasks:    {stats['total']}")
            print(f"Completed:      {stats['completed']} ✅")
            print(f"Pending:        {stats['pending']} ⏳")
            print(f"\nBy Priority:")
            print(f"  🔴 High:   {stats['by_priority']['high']}")
            print(f"  🟡 Medium: {stats['by_priority']['medium']}")
            print(f"  🟢 Low:    {stats['by_priority']['low']}")

        elif choice == "0":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
