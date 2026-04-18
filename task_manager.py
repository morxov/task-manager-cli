"""CLI Task Manager — add, list, complete, and persist tasks with priority."""

import json
import sys
from pathlib import Path

TASKS_FILE = Path.home() / ".task_manager.json"


def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE) as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(description: str, priority: str = "medium"):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "priority": priority.lower(),
        "done": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Added task #{task['id']}: {description} [{priority}]")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'ID':>3}  {'Priority':<8}  {'Done':<5}  Description")
    print("-" * 50)
    for t in tasks:
        status = "✅" if t["done"] else "⬜"
        print(f"{t['id']:>3}  {t['priority']:<8}  {status:<5}  {t['description']}")


def done_task(task_id: int):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            found = True
    if not found:
        print(f"❌ Task #{task_id} not found.")
        return
    save_tasks(tasks)
    print(f"✅ Task #{task_id} marked complete.")


def main():
    commands = {
        "add": lambda args: add_task(" ".join(args[1:]), args[0] if args else "medium"),
        "list": lambda _: list_tasks(),
        "done": lambda args: done_task(int(args[0])) if args else print("Usage: done <id>"),
    }

    if len(sys.argv) < 2:
        print("Usage: task-manager <add|list|done> [args]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd not in commands:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

    commands[cmd](sys.argv[2:])


if __name__ == "__main__":
    main()
