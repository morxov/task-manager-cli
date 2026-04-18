# Task Manager CLI

A simple command-line task manager with priority support.

## Features
- Add tasks with priority (high/medium/low)
- List all tasks with status
- Mark tasks complete
- Persists to `~/.task_manager.json`

## Usage

```bash
python task_manager.py add high Buy groceries
python task_manager.py add Write report
python task_manager.py list
python task_manager.py done 1
```

## Requirements
- Python 3.8+
- pytest (for tests)
